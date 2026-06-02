/**
 * Authentication utility for validating user sessions
 * and preventing access to protected pages after logout
 */

export interface AuthState {
  isAuthenticated: boolean;
  lastCheckTime: number;
}

const AUTH_CHECK_INTERVAL = 30000; // Check auth status every 30 seconds

/**
 * Check if user has a valid authentication cookie
 * This is a client-side check for the access_token cookie
 */
export function hasAuthCookie(): boolean {
  return document.cookie.includes('access_token');
}

/**
 * Get the value of a specific cookie
 */
export function getCookieValue(name: string): string | null {
  const regex = new RegExp(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  const match = document.cookie.match(regex);
  return match ? match[2] : null;
}

/**
 * Clear all authentication data
 */
export function clearAuthData(): void {
  // Clear storage
  sessionStorage.clear();
  localStorage.clear();

  // Delete auth cookies
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const eqPos = cookie.indexOf('=');
    const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
    if (name === 'access_token' || name === 'refresh_token') {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    }
  }
}

/**
 * Validate user session by checking with backend
 */
export async function validateSession(backendUrl: string): Promise<boolean> {
  try {
    const response = await fetch(`${backendUrl}/api/auth/user/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    return response.ok;
  } catch (error) {
    console.error('Session validation error:', error);
    return false;
  }
}

/**
 * Protect a page by redirecting to login if not authenticated
 * Call this at the top of protected pages
 */
export function protectPage(backendUrl: string = import.meta.env.PUBLIC_API_URL): void {
  if (!hasAuthCookie()) {
    // No auth cookie, redirect to login
    window.location.href = '/UserLogin';
    return;
  }

  // Optional: Validate with backend
  validateSession(backendUrl).then((isValid) => {
    if (!isValid) {
      clearAuthData();
      window.location.href = '/UserLogin';
    }
  });
}

/**
 * Set up global protection against back button access to protected pages
 */
export function setupBackButtonProtection(): void {
  const protectedPaths = ['/Customization', '/Gallery', '/Insights', '/UserAccounts'];
  
  // Handle popstate event (back/forward button)
  window.addEventListener('popstate', () => {
    const currentPath = window.location.pathname;
    
    if (protectedPaths.includes(currentPath) && !hasAuthCookie()) {
      // User is trying to access a protected page without auth cookie
      window.location.href = '/UserLogin';
    }
  });

  // Prevent history back navigation by constantly updating history
  window.history.pushState(null, null, window.location.href);
  window.addEventListener('popstate', () => {
    window.history.pushState(null, null, window.location.href);
  });
}

/**
 * Setup page unload handlers to clear sensitive data
 */
export function setupPageUnloadHandlers(): void {
  // Clear data when tab is closed or navigating away from sensitive pages
  window.addEventListener('beforeunload', () => {
    const protectedPaths = ['/Customization', '/Gallery', '/Insights', '/UserAccounts'];
    if (protectedPaths.includes(window.location.pathname)) {
      // Optionally clear data on page unload
      // clearAuthData(); // Uncomment if you want to force logout on page close
    }
  });
}
