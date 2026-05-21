import { LogoIcon } from './Icons.jsx';

export default function AppHeader({ onLogout, showProfileLink = true }) {
  return (
    <header className="app-header">
      <a className="app-header__brand" href="/courses">
        <LogoIcon />
        <span>SkillDrive</span>
      </a>
      <div className="app-header__actions">
        {showProfileLink && (
          <a className="app-header__profile" href="/profile">
            Личный кабинет
          </a>
        )}
        <button type="button" className="app-header__logout" onClick={onLogout}>
          Выйти
        </button>
      </div>
    </header>
  );
}
