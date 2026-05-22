const ICON_MAP = {
  математ: '📐',
  физик: '⚛️',
  информ: '💻',
  русск: '📖',
  истор: '🏛️',
  биолог: '🧬',
  хими: '🧪',
  обществ: '🌍',
  англ: '🇬🇧',
};

export function subjectIcon(subject) {
  if (subject?.icon) {
    return subject.icon;
  }
  const name = (subject?.name || '').toLowerCase();
  for (const [key, emoji] of Object.entries(ICON_MAP)) {
    if (name.includes(key)) {
      return emoji;
    }
  }
  return '📚';
}
