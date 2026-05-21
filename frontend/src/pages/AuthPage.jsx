import { useEffect, useState } from 'react';
import AuthPanel from '../components/AuthPanel.jsx';
import PasswordField from '../components/PasswordField.jsx';
import { MailIcon, UserIcon } from '../components/Icons.jsx';
import { apiPost, apiUrl, saveSession } from '../api/client.js';

export default function AuthPage() {
  const [mode, setMode] = useState('login');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serverOnline, setServerOnline] = useState(null);

  useEffect(() => {
    fetch(apiUrl('/api/v1/health/'))
      .then((res) => setServerOnline(res.ok))
      .catch(() => setServerOnline(false));
  }, []);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [signupForm, setSignupForm] = useState({
    fullName: '',
    email: '',
    password: '',
    password2: '',
    role: 'student',
    grade: '',
  });

  const isLogin = mode === 'login';

  const handleLogin = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await apiPost('/api/v1/accounts/login/', {
        username: loginForm.username.trim(),
        password: loginForm.password,
      });
      saveSession(data);
      window.location.href = '/courses';
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (event) => {
    event.preventDefault();
    setError('');

    if (signupForm.role === 'student' && !signupForm.grade) {
      setError('Укажите класс (8–11) для ученика.');
      return;
    }

    setLoading(true);
    try {
      const email = signupForm.email.trim();
      const [firstName, ...rest] = signupForm.fullName.trim().split(/\s+/);
      const payload = {
        username: email,
        email,
        first_name: firstName || '',
        last_name: rest.join(' ') || '',
        password: signupForm.password,
        password2: signupForm.password2,
        role: signupForm.role,
      };
      if (signupForm.role === 'student') {
        payload.grade = Number(signupForm.grade);
      }
      const data = await apiPost('/api/v1/accounts/register/', payload);
      saveSession(data);
      window.location.href = '/courses';
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <AuthPanel mode={mode} />

        <section className="auth-card">
          <h2 className="auth-card__title">{isLogin ? 'Вход' : 'Регистрация'}</h2>
          <p className="auth-card__subtitle">
            {isLogin
              ? 'Введите свои данные чтобы войти в аккаунт'
              : 'Создайте аккаунт чтобы начать'}
          </p>

          {serverOnline === false && (
            <div className="auth-card__error" role="alert">
              Django не запущен. В терминале:{' '}
              <code>cd django_app</code>, затем{' '}
              <code>uv run python manage.py runserver 127.0.0.1:8000</code>
            </div>
          )}

          {error && (
            <div className="auth-card__error" role="alert">
              {error}
            </div>
          )}

          {isLogin ? (
            <form className="auth-form" onSubmit={handleLogin} noValidate>
              <label className="field" htmlFor="login-username">
                <span className="field__label">Email</span>
                <span className="field__control">
                  <span className="field__icon" aria-hidden="true">
                    <MailIcon />
                  </span>
                  <input
                    id="login-username"
                    type="text"
                    className="field__input"
                    placeholder="Email, указанный при регистрации"
                    value={loginForm.username}
                    onChange={(e) =>
                      setLoginForm((f) => ({ ...f, username: e.target.value }))
                    }
                    autoComplete="username"
                    required
                  />
                </span>
              </label>

              <PasswordField
                id="login-password"
                label="Password"
                placeholder="Введите пароль"
                value={loginForm.password}
                onChange={(e) =>
                  setLoginForm((f) => ({ ...f, password: e.target.value }))
                }
                autoComplete="current-password"
              />

              <button type="submit" className="btn btn--primary" disabled={loading}>
                {loading ? 'Вход…' : 'Log in'}
              </button>
            </form>
          ) : (
            <form className="auth-form" onSubmit={handleSignup} noValidate>
              <label className="field" htmlFor="signup-name">
                <span className="field__label">Full name</span>
                <span className="field__control">
                  <span className="field__icon" aria-hidden="true">
                    <UserIcon />
                  </span>
                  <input
                    id="signup-name"
                    type="text"
                    className="field__input"
                    placeholder="Введите имя пользователя"
                    value={signupForm.fullName}
                    onChange={(e) =>
                      setSignupForm((f) => ({ ...f, fullName: e.target.value }))
                    }
                    autoComplete="name"
                    required
                  />
                </span>
              </label>

              <fieldset className="field role-field">
                <legend className="field__label">Кто вы?</legend>
                <div className="role-options">
                  <label className="role-option">
                    <input
                      type="radio"
                      name="signup-role"
                      value="student"
                      checked={signupForm.role === 'student'}
                      onChange={() =>
                        setSignupForm((f) => ({ ...f, role: 'student' }))
                      }
                    />
                    <span>Ученик</span>
                  </label>
                  <label className="role-option">
                    <input
                      type="radio"
                      name="signup-role"
                      value="parent"
                      checked={signupForm.role === 'parent'}
                      onChange={() =>
                        setSignupForm((f) => ({ ...f, role: 'parent', grade: '' }))
                      }
                    />
                    <span>Родитель</span>
                  </label>
                </div>
              </fieldset>

              {signupForm.role === 'student' && (
                <label className="field" htmlFor="signup-grade">
                  <span className="field__label">Класс</span>
                  <select
                    id="signup-grade"
                    className="field__input field__input--select"
                    value={signupForm.grade}
                    onChange={(e) =>
                      setSignupForm((f) => ({ ...f, grade: e.target.value }))
                    }
                    required
                  >
                    <option value="" disabled>
                      Выберите класс
                    </option>
                    {[8, 9, 10, 11].map((n) => (
                      <option key={n} value={String(n)}>
                        {n} класс
                      </option>
                    ))}
                  </select>
                </label>
              )}

              <label className="field" htmlFor="signup-email">
                <span className="field__label">Email address</span>
                <span className="field__control">
                  <span className="field__icon" aria-hidden="true">
                    <MailIcon />
                  </span>
                  <input
                    id="signup-email"
                    type="email"
                    className="field__input"
                    placeholder="Введите свой email"
                    value={signupForm.email}
                    onChange={(e) =>
                      setSignupForm((f) => ({ ...f, email: e.target.value }))
                    }
                    autoComplete="email"
                    required
                  />
                </span>
              </label>

              <PasswordField
                id="signup-password"
                label="Password"
                placeholder="Придумайте пароль"
                value={signupForm.password}
                onChange={(e) =>
                  setSignupForm((f) => ({ ...f, password: e.target.value }))
                }
                autoComplete="new-password"
              />

              <PasswordField
                id="signup-password2"
                label="Confirm password"
                placeholder="Подтвердите пароль"
                value={signupForm.password2}
                onChange={(e) =>
                  setSignupForm((f) => ({ ...f, password2: e.target.value }))
                }
                autoComplete="new-password"
              />

              <button type="submit" className="btn btn--primary" disabled={loading}>
                {loading ? 'Создание аккаунта…' : 'Регистрация'}
              </button>
            </form>
          )}

          <p className="auth-card__footer">
            {isLogin ? (
              <>
                Don&apos;t have an account?{' '}
                <button
                  type="button"
                  className="link link--button"
                  onClick={() => {
                    setMode('signup');
                    setError('');
                  }}
                >
                  Sign up
                </button>
              </>
            ) : (
              <>
                Already have an account?{' '}
                <button
                  type="button"
                  className="link link--button"
                  onClick={() => {
                    setMode('login');
                    setError('');
                  }}
                >
                  Log in
                </button>
              </>
            )}
          </p>
        </section>
      </div>
    </div>
  );
}
