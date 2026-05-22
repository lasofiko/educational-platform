import { useEffect, useState } from 'react';
import AuthPage from './pages/AuthPage.jsx';
import CourseSelectionPage from './pages/CourseSelectionPage.jsx';
import ProfilePage from './pages/ProfilePage.jsx';
import { getAccessToken } from './api/client.js';

function resolveRoute() {
  const path = window.location.pathname;
  const hasToken = !!getAccessToken();

  if (path === '/login') {
    return hasToken ? 'courses' : 'auth';
  }
  if (path === '/courses') {
    return hasToken ? 'courses' : 'auth';
  }
  if (path === '/profile') {
    return hasToken ? 'profile' : 'auth';
  }
  if (path === '/' || path === '') {
    return hasToken ? 'courses' : 'auth';
  }
  return hasToken ? 'courses' : 'auth';
}

export default function App() {
  const [route, setRoute] = useState(resolveRoute);

  useEffect(() => {
    const onNavigate = () => setRoute(resolveRoute());
    window.addEventListener('popstate', onNavigate);
    return () => window.removeEventListener('popstate', onNavigate);
  }, []);

  if (route === 'auth') {
    return <AuthPage />;
  }
  if (route === 'profile') {
    return <ProfilePage />;
  }
  return <CourseSelectionPage />;
}
