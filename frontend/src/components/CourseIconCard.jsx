export default function CourseIconCard({ tile, enrolled, loading, onOpen }) {
  const { subject, title, description, icon, accent, available } = tile;

  return (
    <article
      className={`course-icon-card${enrolled ? ' course-icon-card--enrolled' : ''}${!available ? ' course-icon-card--soon' : ''}${loading ? ' course-icon-card--loading' : ''}`}
      style={{ '--course-accent': accent }}
    >
      <button
        type="button"
        className="course-icon-card__icon-btn"
        disabled={!available || loading}
        onClick={() => onOpen(tile)}
        aria-label={`Перейти к обучению: ${title}`}
      >
        <span className="course-icon-card__icon" aria-hidden="true">
          {icon}
        </span>
      </button>

      <h3 className="course-icon-card__title">{title}</h3>
      <p className="course-icon-card__desc">{description}</p>

      {enrolled && <span className="course-icon-card__badge">В процессе</span>}
      {!available && <span className="course-icon-card__badge course-icon-card__badge--muted">Скоро</span>}

      <button
        type="button"
        className="btn btn--primary course-icon-card__action"
        disabled={!available || loading}
        onClick={() => onOpen(tile)}
      >
        {loading ? 'Открываем…' : enrolled ? 'Продолжить' : 'Начать обучение'}
      </button>
    </article>
  );
}
