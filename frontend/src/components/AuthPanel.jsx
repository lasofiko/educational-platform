import { LogoIcon, FeatureIcon } from './Icons.jsx';

const FEATURES = [
  { key: 'ai', text: 'Готовься к экзаменам' },
  { key: 'progress', text: 'Отслеживай свой прогресс' },
  { key: 'anywhere', text: 'Учись где угодно' },
];

export default function AuthPanel({ mode }) {
  const isLogin = mode === 'login';

  return (
    <aside className="auth-panel">
      <div className="auth-panel__bg" aria-hidden="true" />
      <div className="auth-panel__content">
        <div className="brand">
          <LogoIcon />
          <span className="brand__name">SkillDrive</span>
        </div>

        <h1 className="auth-panel__title">
          {isLogin ? 'Добро пожаловать' : 'Создать аккаунт'}
        </h1>
        <p className="auth-panel__subtitle">
          {isLogin
            ? 'Войти и продолжить обучение'
            : 'Начать обучение'}
        </p>

        <ul className="features">
          {FEATURES.map((item) => (
            <li key={item.key} className="features__item">
              <FeatureIcon type={item.key} />
              <span>{item.text}</span>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
