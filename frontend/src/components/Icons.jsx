export function LogoIcon() {
  return (
    <svg className="logo-icon" viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <path
        d="M16 3L28 9v14l-12 6L4 23V9l12-6z"
        stroke="currentColor"
        strokeWidth="1.5"
        fill="rgba(45, 92, 97, 0.35)"
      />
      <path
        d="M12 14h8v2a4 4 0 01-8 0v-2zM13 12c0-1.1.9-2 2-2h2a2 2 0 010 4h-2a2 2 0 01-2-2z"
        fill="currentColor"
      />
      <path d="M10 22h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export function MailIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path
        d="M3 5.5A2.5 2.5 0 015.5 3h9A2.5 2.5 0 0117 5.5v9a2.5 2.5 0 01-2.5 2.5h-9A2.5 2.5 0 013 14.5v-9z"
        stroke="currentColor"
        strokeWidth="1.3"
      />
      <path d="M4 6.5l6 4 6-4" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  );
}

export function LockIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <rect x="4.5" y="9" width="11" height="8" rx="2" stroke="currentColor" strokeWidth="1.3" />
      <path
        d="M7 9V7a3 3 0 116 0v2"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function UserIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <circle cx="10" cy="7" r="3" stroke="currentColor" strokeWidth="1.3" />
      <path
        d="M4.5 16.5c.8-2.5 2.8-4 5.5-4s4.7 1.5 5.5 4"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function EyeIcon({ open }) {
  if (open) {
    return (
      <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path
          d="M2.5 10s3-5 7.5-5 7.5 5 7.5 5-3 5-7.5 5S2.5 10 2.5 10z"
          stroke="currentColor"
          strokeWidth="1.3"
        />
        <circle cx="10" cy="10" r="2.5" stroke="currentColor" strokeWidth="1.3" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path
        d="M3 14l2.5-2M17 14l-2.5-2M7 7l1.5-1.5M13 7L11.5 5.5"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
      <path
        d="M2.5 10s3-5 7.5-5c2 0 3.7.8 5 2"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function FeatureIcon({ type }) {
  const paths = {
    ai: 'M6 14V8l4-2v8M14 14V6l4 2v6',
    roadmap: 'M4 14h3V8H4v6zm5 0h3V5H9v9zm5 0h3V10h-3v4z',
    progress: 'M4 14V10l4-2 4 2v4M16 6v8',
    anywhere: 'M4 10a6 6 0 1012 0M10 4v2M10 14v2M16 6l-1.5 1.5M6 14l1.5-1.5',
  };
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" className="feature-icon">
      <path d={paths[type]} stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
