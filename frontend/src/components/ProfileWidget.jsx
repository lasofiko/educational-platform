export default function ProfileWidget({ profile, loading }) {
  const name =
    profile?.user?.first_name ||
    profile?.user?.username ||
    'Пользователь';
  const roleLabel = profile?.role_display;
  const grade =
    profile?.role === 'student' && profile?.grade
      ? `${profile.grade} класс`
      : null;

  return (
    <a className="profile-widget" href="/profile">
      <span className="profile-widget__icon" aria-hidden="true">
        👤
      </span>
      <span className="profile-widget__body">
        <span className="profile-widget__label">Личный кабинет</span>
        {loading ? (
          <span className="profile-widget__meta">Загрузка…</span>
        ) : (
          <span className="profile-widget__meta">
            {name}
            {roleLabel ? ` · ${roleLabel}` : ''}
            {grade ? ` · ${grade}` : ''}
          </span>
        )}
      </span>
      <span className="profile-widget__arrow" aria-hidden="true">
        →
      </span>
    </a>
  );
}
