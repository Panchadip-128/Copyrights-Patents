"use client";
import Link from 'next/link';

export default function ReportsPage() {
  return (
    <div style={{ minHeight: '100vh', padding: '2rem', background: 'var(--bg-main)', fontFamily: 'var(--font-inter)' }}>
      <header style={{ borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
            <div style={{ width: '40px', height: '40px', background: 'var(--accent-purple)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold' }}>AX</div>
            <h1 style={{ color: 'white', fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>
            ARICCA-X Intelligence Reports
            </h1>
        </div>
        <p style={{ color: 'var(--text-muted)', marginLeft: '56px' }}>
          Historical patent-pending credibility analysis logs and deterministic audit trails.
        </p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.5rem' }}>
        
        {/* Report Card 1 */}
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', padding: '1.5rem', borderRadius: 'var(--radius-lg)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <span style={{ background: 'var(--accent-rose)', color: 'white', padding: '4px 10px', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 'bold', letterSpacing: '1px' }}>HIGH RISK</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Oct 02, 2026</span>
          </div>
          <h3 style={{ color: 'white', fontSize: '1.15rem', marginBottom: '0.5rem', lineHeight: '1.4' }}>Global Tech Journal of Advanced Research</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            Flags: Temporal Impossibility (PRLV), Geospatial Dissonance
          </p>
          <button style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--accent-blue)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '10px 16px', borderRadius: '6px', cursor: 'pointer', width: '100%', fontWeight: '600', transition: 'all 0.2s' }}>View Full Audit Archive</button>
        </div>

        {/* Report Card 2 */}
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', padding: '1.5rem', borderRadius: 'var(--radius-lg)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <span style={{ background: 'var(--accent-emerald)', color: 'white', padding: '4px 10px', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 'bold', letterSpacing: '1px' }}>VERIFIED</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Oct 01, 2026</span>
          </div>
          <h3 style={{ color: 'white', fontSize: '1.15rem', marginBottom: '0.5rem', lineHeight: '1.4' }}>IEEE Transactions on Software Engineering</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            Flags: None. Baseline deterministic credibility confirmed.
          </p>
          <button style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--accent-blue)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '10px 16px', borderRadius: '6px', cursor: 'pointer', width: '100%', fontWeight: '600', transition: 'all 0.2s' }}>View Full Audit Archive</button>
        </div>

      </div>

      <div style={{ marginTop: '3rem' }}>
        <Link href="/" style={{ color: 'var(--accent-blue)', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          <svg style={{ width: '16px', height: '16px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          Return to Main Dashboard
        </Link>
      </div>
    </div>
  );
}
