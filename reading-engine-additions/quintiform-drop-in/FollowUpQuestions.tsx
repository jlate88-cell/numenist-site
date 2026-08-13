'use client';

/**
 * components/FollowUpQuestions.tsx
 *
 * React (Next.js App Router, client-side) component for the 5 follow-up
 * questions feature. Drops into the reading page after the closing section.
 *
 * Props expect ONE of: reading_cache_id OR astrology_cache_id, matching
 * which cache table the reading lives in.
 *
 * Tailwind classes used here mirror the Numen palette; adjust to whatever
 * className conventions quintiform's design system already uses.
 */

import { useState } from 'react';

interface FollowUp {
  id: string;
  question_index: number;
  question: string;
  answer: string;
  answered_at: string;
}

interface Props {
  readingCacheId?: string | null;       // for the 17-section flagship
  astrologyCacheId?: string | null;     // for the 15-section combined astrology
  initialFollowUps?: FollowUp[];        // pre-loaded from server on first paint
}

export default function FollowUpQuestions(props: Props) {
  const [followUps, setFollowUps] = useState<FollowUp[]>(props.initialFollowUps ?? []);
  const [question, setQuestion] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const used = followUps.length;
  const remaining = 5 - used;
  const nextIndex = used + 1;
  const cacheId = props.readingCacheId ?? props.astrologyCacheId;

  async function askQuestion() {
    if (!cacheId) {
      setError('Missing reading id — refresh and try again.');
      return;
    }
    if (!question.trim()) return;
    if (remaining <= 0) return;

    setSubmitting(true);
    setError(null);

    try {
      const res = await fetch(`/api/readings/${cacheId}/followups`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_index: nextIndex,
          question: question.trim(),
          reading_cache_id:   props.readingCacheId   ?? null,
          astrology_cache_id: props.astrologyCacheId ?? null,
        }),
      });

      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j.error ?? `request failed (${res.status})`);
      }

      const row: FollowUp = await res.json();
      setFollowUps([...followUps, row]);
      setQuestion('');
    } catch (e: any) {
      setError(e.message ?? String(e));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="reading-section follow-up-section">
      <h2>Five Follow-Up Questions</h2>
      <p className="kicker">
        Ask up to 5 questions to deepen this reading. Each is answered in the
        reading&apos;s own voice, grounded in the chart you were given.{' '}
        <strong>{used} / 5 used.</strong>
      </p>

      {followUps.map((f) => (
        <details
          key={f.id}
          className="followup-card"
          open={f.question_index === used}
          style={{
            margin: '18px 0',
            padding: '14px 18px',
            background: 'rgba(212,168,87,0.06)',
            border: '1px solid rgba(212,168,87,0.18)',
            borderRadius: 12,
          }}
        >
          <summary
            style={{
              cursor: 'pointer',
              fontFamily: '"Cormorant Garamond", serif',
              fontSize: 18,
              color: '#d4a857',
              marginBottom: 8,
            }}
          >
            Q{f.question_index}. {f.question}
          </summary>
          <div
            style={{
              fontFamily: '"Cormorant Garamond", serif',
              fontSize: 16,
              lineHeight: 1.65,
              color: '#c9bfa8',
              whiteSpace: 'pre-wrap',
              marginTop: 10,
            }}
          >
            {f.answer}
          </div>
        </details>
      ))}

      {remaining > 0 ? (
        <div style={{ marginTop: 18 }}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder={`Question ${nextIndex} of 5 — what do you want clarity on?`}
            rows={3}
            style={{
              width: '100%',
              padding: '12px 14px',
              background: 'rgba(13,4,32,0.7)',
              border: '1px solid rgba(212,168,87,0.18)',
              borderRadius: 10,
              color: '#f4ecd8',
              fontFamily: '"Cormorant Garamond", serif',
              fontSize: 16,
            }}
            disabled={submitting}
          />
          <div style={{ marginTop: 10, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <small style={{ color: '#6b6480', fontFamily: 'Inter, sans-serif' }}>
              {remaining} {remaining === 1 ? 'question' : 'questions'} remaining
            </small>
            <button
              onClick={askQuestion}
              disabled={submitting || !question.trim()}
              style={{
                padding: '10px 22px',
                background: '#d4a857',
                color: '#06010f',
                border: 'none',
                borderRadius: 30,
                cursor: submitting || !question.trim() ? 'not-allowed' : 'pointer',
                fontFamily: 'Inter, sans-serif',
                fontSize: 12,
                letterSpacing: 2,
                textTransform: 'uppercase',
                fontWeight: 600,
                opacity: submitting || !question.trim() ? 0.5 : 1,
              }}
            >
              {submitting ? 'Composing…' : 'Ask →'}
            </button>
          </div>
          {error && (
            <p style={{ color: '#c75d7a', marginTop: 8, fontFamily: 'Inter, sans-serif', fontSize: 13 }}>
              {error}
            </p>
          )}
        </div>
      ) : (
        <p style={{ color: '#6b6480', fontFamily: 'Inter, sans-serif', fontSize: 13, marginTop: 18 }}>
          You&apos;ve used all 5 questions for this reading.
        </p>
      )}
    </section>
  );
}
