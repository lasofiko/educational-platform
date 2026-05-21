import { useState } from 'react';
import { EyeIcon, LockIcon } from './Icons.jsx';

export default function PasswordField({
  id,
  label,
  placeholder,
  value,
  onChange,
  autoComplete,
}) {
  const [visible, setVisible] = useState(false);

  return (
    <label className="field" htmlFor={id}>
      <span className="field__label">{label}</span>
      <span className="field__control">
        <span className="field__icon" aria-hidden="true">
          <LockIcon />
        </span>
        <input
          id={id}
          type={visible ? 'text' : 'password'}
          className="field__input"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          autoComplete={autoComplete}
          required
        />
        <button
          type="button"
          className="field__toggle"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? 'Скрыть пароль' : 'Показать пароль'}
        >
          <EyeIcon open={visible} />
        </button>
      </span>
    </label>
  );
}
