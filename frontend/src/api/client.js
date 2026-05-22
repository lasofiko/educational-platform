const API_BASE = (import.meta.env.VITE_API_BASE || '').replace(/\/$/, '');

export function apiUrl(path) {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return API_BASE ? `${API_BASE}${normalized}` : normalized;
}

export function getAccessToken() {
  return localStorage.getItem('access_token');
}

export function clearSession() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('selected_subject_id');
  localStorage.removeItem('selected_subject_name');
}

export function saveSession(data) {
  if (data.access) {
    localStorage.setItem('access_token', data.access);
  }
  if (data.refresh) {
    localStorage.setItem('refresh_token', data.refresh);
  }
}

export function formatApiError(data, fallback = 'Ошибка запроса') {
  if (!data || typeof data !== 'object') {
    return fallback;
  }
  if (typeof data.error === 'string') {
    return data.error;
  }
  if (data.error?.detail) {
    return String(data.error.detail);
  }
  if (typeof data.detail === 'string') {
    return data.detail;
  }
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg || JSON.stringify(item)).join(', ');
  }

  const parts = [];
  for (const [key, value] of Object.entries(data)) {
    if (key === 'error' || key === 'detail') {
      continue;
    }
    const text = Array.isArray(value) ? value.join(' ') : String(value);
    const label = key === 'non_field_errors' ? '' : `${key}: `;
    parts.push(`${label}${text}`.trim());
  }
  return parts.length ? parts.join('; ') : fallback;
}

export async function apiRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };
  const token = getAccessToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const url = apiUrl(path);

  let response;
  try {
    response = await fetch(url, {
      ...options,
      headers,
    });
  } catch {
    throw new Error(
      `Не удалось связаться с ${url}`
      );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    let message = formatApiError(data);
    if (response.status === 404) {
      message = `Сервер не нашёл адрес ${url}. Проверьте, что Django запущен на порту 8003.`;
    }
    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

export async function apiPost(path, body) {
  return apiRequest(path, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
