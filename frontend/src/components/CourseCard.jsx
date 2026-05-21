import { subjectIcon } from '../utils/subjectIcon.js';

export default function CourseCard({
  subject,
  enrolled,
  loading,
  onSelect,
}) {
  return (
    <article
      className={`course-card${enrolled ? ' course-card--enrolled' : ''}${loading ? ' course-card--loading' : ''}`}
    >
      <div className="course-card__icon" aria-hidden="true">
        {subjectIcon(subject)}
      </div>
      <h3 className="course-card__title">{subject.name}</h3>
      {subject.description && (
        <p className="course-card__desc">{subject.description}</p>
      )}
      {enrolled && <span className="course-card__badge">Уже записаны</span>}
      <button
        type="button"
        className="btn btn--primary course-card__btn"
        disabled={loading}
        onClick={() => onSelect(subject)}
      >
        {loading ? 'Загрузка…' : enrolled ? 'Продолжить' : 'Начать обучение'}
      </button>
    </article>
  );
}
