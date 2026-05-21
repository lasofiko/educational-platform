import { useEffect, useState } from 'react';
import AppHeader from '../components/AppHeader.jsx';
import { apiRequest, clearSession } from '../api/client.js';

function parseList(data) {
  if (Array.isArray(data)) return data;
  if (data?.results) return data.results;
  return [];
}

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [enrollments, setEnrollments] = useState([]);
  const [subjectNames, setSubjectNames] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const [me, enrollData, subjectsData] = await Promise.all([
          apiRequest('/api/v1/accounts/me/'),
          apiRequest('/api/v1/progress/enrollments/').catch(() => ({ results: [] })),
          apiRequest('/api/v1/courses/subjects/').catch(() => ({ results: [] })),
        ]);
        setProfile(me);
        setEnrollments(parseList(enrollData));
        const names = {};
        parseList(subjectsData).forEach((s) => {
          names[s.id] = s.name;
        });
        setSubjectNames(names);
      } catch (err) {
        if (err.status === 401) {
          clearSession();
          window.location.href = '/login';
          return;
        }
        setError(err.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleLogout = () => {
    clearSession();
    window.location.href = '/login';
  };

  const user = profile?.user;

  return (
    <div className="courses-page">
      <AppHeader onLogout={handleLogout} showProfileLink={false} />

      <main className="courses-main">
        <a className="link courses-back" href="/courses">
          ← К выбору курса
        </a>

        <div className="profile-page-card">
          <h1>Личный кабинет</h1>

          {error && (
            <div className="courses-error" role="alert">
              {error}
            </div>
          )}

          {loading ? (
            <p className="courses-status">Загружаем данные…</p>
          ) : (
            <>
              <section className="profile-section">
                <h2>Профиль</h2>
                <dl className="profile-dl">
                  <div>
                    <dt>Имя</dt>
                    <dd>
                      {[user?.first_name, user?.last_name].filter(Boolean).join(' ') ||
                        '—'}
                    </dd>
                  </div>
                  <div>
                    <dt>Email</dt>
                    <dd>{user?.email || user?.username || '—'}</dd>
                  </div>
                  <div>
                    <dt>Роль</dt>
                    <dd>{profile?.role_display || '—'}</dd>
                  </div>
                  <div>
                    <dt>Класс</dt>
                    <dd>
                      {profile?.role === 'student' && profile?.grade
                        ? `${profile.grade}`
                        : profile?.role === 'parent'
                          ? '—'
                          : profile?.grade
                            ? `${profile.grade}`
                            : '—'}
                    </dd>
                  </div>
                  <div>
                    <dt>Целевой балл</dt>
                    <dd>{profile?.target_score ?? '—'}</dd>
                  </div>
                </dl>
              </section>

              <section className="profile-section">
                <h2>Мои курсы</h2>
                {enrollments.length === 0 ? (
                  <p className="courses-status">Вы ещё не записаны на курс.</p>
                ) : (
                  <ul className="profile-courses-list">
                    {enrollments.map((item) => (
                      <li key={item.id}>
                        <a href={`/roadmap?subject=${item.subject}`}>
                          {subjectNames[item.subject] || `Курс #${item.subject}`}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
