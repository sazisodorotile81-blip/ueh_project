const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'
export function token() { return sessionStorage.getItem('access') }
export async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (token()) headers.Authorization = `Bearer ${token()}`
  const response = await fetch(`${API}${path}`, { ...options, headers })
  const data = response.status === 204 ? null : await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || JSON.stringify(data) || 'Request failed')
  return data
}
export async function login(username, password) {
  const data = await api('/auth/token/', { method: 'POST', body: JSON.stringify({ username, password }) })
  sessionStorage.setItem('access', data.access); sessionStorage.setItem('refresh', data.refresh)
  return api('/auth/me/')
}
export function logout() { sessionStorage.clear() }
