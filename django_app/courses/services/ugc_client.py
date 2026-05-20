import os

import requests

DEFAULT_UGC_SUMMARY = {
    'review_count': 0,
    'avg_rating': None,
    'comment_count': 0,
}


def _fetch_results(base_url, path, target_type, target_id, timeout):
    response = requests.get(
        f'{base_url}{path}',
        params={'target_type': target_type, 'target_id': target_id},
        timeout=timeout,
    )
    if response.status_code != 200:
        return None
    return response.json().get('results', [])


def get_ugc_summary(target_type, target_id, base_url=None, timeout=1.0):
    """
    Сводка UGC для detail Lesson/Subject.
    При недоступности Flask возвращает нули и avg_rating=null.
    """
    base = (base_url or os.environ.get('UGC_BASE_URL', 'http://localhost:8001')).rstrip('/')
    try:
        reviews = _fetch_results(
            base, '/api/v1/ugc/reviews', target_type, target_id, timeout,
        )
        comments = _fetch_results(
            base, '/api/v1/ugc/comments', target_type, target_id, timeout,
        )
    except requests.RequestException:
        return dict(DEFAULT_UGC_SUMMARY)

    if reviews is None and comments is None:
        return dict(DEFAULT_UGC_SUMMARY)

    review_rows = reviews or []
    ratings = [row['rating'] for row in review_rows if row.get('rating') is not None]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

    return {
        'review_count': len(review_rows),
        'avg_rating': avg_rating,
        'comment_count': len(comments or []),
    }
