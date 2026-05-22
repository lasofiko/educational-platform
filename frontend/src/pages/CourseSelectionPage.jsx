import { useCallback, useEffect, useState } from 'react';
import AppHeader from '../components/AppHeader.jsx';
import CourseIconCard from '../components/CourseIconCard.jsx';
import ProfileWidget from '../components/ProfileWidget.jsx';
import { buildCourseTiles } from '../data/courseCatalog.js';
import { apiPost, apiRequest, clearSession } from '../api/client.js';

function parseList(data) {
  if (Array.isArray(data)) {
    return data;
  }
  if (data?.results) {
    return data.results;
  }
  return [];
}

export default function CourseSelectionPage() {
  const [tiles, setTiles] = useState([]);
  const [enrolledIds, setEnrolledIds] = useState(new Set());
  const [profile, setProfile] = useState(null);
  const [loadingId, setLoadingId] = useState(null);
  const [pageLoading, setPageLoading] = useState(true);
  const [profileLoading, setProfileLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = useCallback(async () => {
    setPageLoading(true);
    setProfileLoading(true);
    setError('');
    try {
      const [subjectsData, enrollmentsData, profileData] = await Promise.all([
        apiRequest('/api/v1/courses/subjects/'),
        apiRequest('/api/v1/progress/enrollments/').catch(() => ({ results: [] })),
        apiRequest('/api/v1/accounts/me/').catch(() => null),
      ]);
      const apiSubjects = parseList(subjectsData);
      setTiles(buildCourseTiles(apiSubjects));
      setEnrolledIds(new Set(parseList(enrollmentsData).map((row) => row.subject)));
      setProfile(profileData);
    } catch (err) {
      if (err.status === 401) {
        clearSession();
        window.location.href = '/login';
        return;
      }
      setError(err.message);
    } finally {
      setPageLoading(false);
      setProfileLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleLogout = () => {
    clearSession();
    window.location.href = '/login';
  };

  const openCourse = async (tile) => {
    const { subject, available, title } = tile;

    setLoadingId(subject.id);
    setError('');
    try {
      if (!enrolledIds.has(subject.id)) {
        await apiPost('/api/v1/progress/enrollments/', { subject: subject.id });
        setEnrolledIds((prev) => new Set([...prev, subject.id]));
      }
      localStorage.setItem('selected_subject_id', String(subject.id));
      localStorage.setItem('selected_subject_name', subject.name);
      window.location.href = `/roadmap?subject=${subject.id}`;
    } catch (err) {
      if (err.status === 409) {
        setEnrolledIds((prev) => new Set([...prev, subject.id]));
        localStorage.setItem('selected_subject_id', String(subject.id));
        window.location.href = `/roadmap?subject=${subject.id}`;
      return;
      }
      setError(err.message);
    } finally {
      setLoadingId(null);
    }
  };

  return (
    <div className="courses-page">
      <AppHeader onLogout={handleLogout} />

      <main className="courses-main">
        <div className="courses-top">
          <div className="courses-intro">
            <h1>Выберите курс</h1>
            <p>
              Нажмите на иконку предмета, чтобы перейти к обучению: математика,
              русский язык или информатика.
            </p>
          </div>
          <ProfileWidget profile={profile} loading={profileLoading} />
        </div>

        {error && (
          <div className="courses-error" role="alert">
            {error}
          </div>
        )}

        {pageLoading ? (
          <p className="courses-status">Загружаем курсы…</p>
        ) : (
          <div className="courses-icon-grid">
            {tiles.map((tile) => (
              <CourseIconCard
                key={tile.slug}
                tile={tile}
                enrolled={tile.subject?.id && enrolledIds.has(tile.subject.id)}
                loading={loadingId === tile.subject?.id}
                onOpen={openCourse}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
