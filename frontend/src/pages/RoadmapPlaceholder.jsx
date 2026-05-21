import AppHeader from '../components/AppHeader.jsx';
import { clearSession } from '../api/client.js';

export default function RoadmapPlaceholder() {
  const params = new URLSearchParams(window.location.search);
  const subjectName =
    localStorage.getItem('selected_subject_name') || `курс #${params.get('subject') || '?'}`;

  const handleLogout = () => {
    clearSession();
    window.location.href = '/login';
  };

  return (
    <div className="courses-page">
      <AppHeader onLogout={handleLogout} />
      <main className="courses-main courses-main--center">
        <div className="roadmap-placeholder">
          <h1>{subjectName}</h1>
          <p>Страница обучения по предмету. Дорожная карта и уроки — в следующих спринтах.</p>
          <a className="btn btn--primary" href="/courses">
            ← К выбору курса
          </a>
        </div>
      </main>
    </div>
  );
}
