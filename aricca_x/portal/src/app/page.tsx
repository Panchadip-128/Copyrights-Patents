"use client";
import { useEffect, useRef } from 'react';

export default function Home() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = '/aricca_logic.js';
    document.body.appendChild(script);
    
    // Simulate initial tab click to setup active state
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue')?.click();
        }
    }, 200);

    return () => {
      if (document.body.contains(script)) {
          document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `

<div id="auth-container">
    <div class="auth-card" id="login-box">
        <div style="display:flex; justify-content:center; margin-bottom:1.5rem;">
            <div class="logo-icon" style="width:56px;height:56px;font-size:1.5rem;">AX</div>
        </div>
        <h2>ARICCA-X Secure Login</h2>
        <p>Role-Based System Access Verification</p>
        <div class="demo-box">
            <strong>Demo Credentials (Testing Only):</strong>
            Admin Role: <em>admin@aricca.com / admin123</em><br>
            User Role: <em>user@aricca.com / user123</em>
        </div>
        <form class="auth-form" id="login-form" onsubmit="window.handleLogin(event)">
            <input type="email" id="login-email" placeholder="Email Address" required>
            <input type="password" id="login-pwd" placeholder="Password" required>
            <button class="btn btn-primary" type="submit">Authenticate & Enter</button>
            <div id="login-error" style="color:var(--accent-rose); font-size:0.85rem; margin-top:12px; text-align:center; display:none; font-weight: 600;">Invalid credentials or role not recognized.</div>
        </form>
        <div class="auth-switch" onclick="toggleAuth('signup')">Need system access? <span>Request Account</span></div>
    </div>

    <div class="auth-card" id="signup-box" style="display: none;">
        <div style="display:flex; justify-content:center; margin-bottom:1.5rem;">
            <div class="logo-icon" style="width:56px;height:56px;font-size:1.5rem;">AX</div>
        </div>
        <h2>Request Access</h2>
        <p>ARICCA-X is currently in closed beta.</p>
        <form class="auth-form" id="signup-form">
            <input type="text" placeholder="Full Name" required>
            <input type="email" placeholder="Institutional Email" required>
            <input type="text" placeholder="Institution / Organization" required>
            <button class="btn btn-primary" type="button" onclick="alert('Signup requests are queued for manual administrative review in Demo Mode.')">Submit Request</button>
        </form>
        <div class="auth-switch" onclick="toggleAuth('login')">Already approved? <span>Login Here</span></div>
    </div>
</div>
    `}} />
  );
}
