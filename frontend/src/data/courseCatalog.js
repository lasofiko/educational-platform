/** Каталог предметов на странице выбора курса */
export const COURSE_CATALOG = [
  {
    slug: 'math',
    title: 'Математика',
    description: 'Алгебра, геометрия и задачи ЕГЭ профильного уровня',
    icon: '📐',
    accent: '#2d5c61',
    matchKeys: ['математ'],
  },
  {
    slug: 'russian',
    title: 'Русский язык',
    description: 'Орфография, пунктуация и сочинение',
    icon: '📖',
    accent: '#3d6a6f',
    matchKeys: ['русск'],
  },
  {
    slug: 'informatics',
    title: 'Информатика',
    description: 'Программирование, алгоритмы и логика',
    icon: '💻',
    accent: '#4a858c',
    matchKeys: ['информ'],
  },
];

export function buildCourseTiles(apiSubjects) {
  return COURSE_CATALOG.map((catalogItem) => {
    const match = apiSubjects.find((subject) =>
      catalogItem.matchKeys.some((key) =>
        subject.name.toLowerCase().includes(key),
      ),
    );

    return {
      ...catalogItem,
      subject: match || {
        id: null,
        name: catalogItem.title,
        description: catalogItem.description,
      },
      available: Boolean(match),
    };
  });
}
