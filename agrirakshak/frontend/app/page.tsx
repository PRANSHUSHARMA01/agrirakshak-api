import Link from "next/link";
import {
  ArrowRight,
  Bot,
  Camera,
  ChevronRight,
  CloudSun,
  FileText,
  HeartHandshake,
  Leaf,
  Map,
  Search,
  ShieldCheck,
} from "lucide-react";

function Brand({ light = false }: { light?: boolean }) {
  return (
    <Link href="/" className={`brand ${light ? "brand-light" : ""}`}>
      <img src="/agrirakshak-logo.png" alt="AgriRakshak Logo" />
      <span>
        Agri<span>Rakshak</span>
      </span>
    </Link>
  );
}

function PublicHeader() {
  return (
    <header className="public-header">
      <Brand />
      <nav>
        <a href="#how-it-works">How it works</a>
        <a href="#features">What we help with</a>
        <Link href="/login">Sign in</Link>
      </nav>
      <Link href="/farmer/diagnose" className="button button-small button-ink">
        Scan my crop <ArrowRight size={16} />
      </Link>
    </header>
  );
}

export default function LandingPage() {
  return (
    <div className="landing">
      <PublicHeader />

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="eyebrow-line" /> Smart crop care for India
          </div>
          <h1>
            See the signs early.<br />
            <em>Protect the season.</em>
          </h1>
          <p>
            AI-powered crop disease detection, weather risk alerts, and expert agricultural guidance—made clear for the people who grow our food.
          </p>
          <div className="hero-actions">
            <Link href="/farmer/diagnose" className="button button-ink">
              Scan my crop <ArrowRight size={18} />
            </Link>
            <Link href="/farmer/chat" className="text-link">
              Talk to AgriRakshak <span>↗</span>
            </Link>
          </div>
          <div className="trust-line">
            <ShieldCheck size={16} /> Built for farmers, with agricultural officers
          </div>
        </div>

        <div className="hero-visual">
          <img src="/agrirakshak-hero.jpg" alt="Farmer holding a rice leaf in a paddy field" />
          <div className="hero-note note-top">
            <span className="note-kicker">Today's field note</span>
            <strong>Early signs are<br />worth noticing.</strong>
          </div>
          <div className="hero-note note-bottom">
            <div className="mini-signal">
              <span />Low risk today
            </div>
            <span className="note-place">Karnal · Haryana</span>
          </div>
        </div>
      </section>

      {/* How It Works Workflow */}
      <section id="how-it-works" className="workflow-section">
        <div className="section-intro">
          <span className="section-label">How it works</span>
          <h2>From a crop photo<br />to a clearer next step.</h2>
        </div>
        <div className="workflow-steps">
          {[
            ["01", "Capture", "Take a clear photo of the affected leaf."],
            ["02", "Analyze", "Our AI looks for familiar signs and patterns."],
            ["03", "Understand", "See what it could mean, in simple language."],
            ["04", "Act", "Follow safe next steps or ask an expert."],
          ].map(([num, title, copy], i) => (
            <div className="workflow-step" key={num}>
              <span className="step-num">{num}</span>
              <div className="step-icon">
                {i === 0 ? <Camera size={21} /> : i === 1 ? <Search size={21} /> : i === 2 ? <FileText size={21} /> : <HeartHandshake size={21} />}
              </div>
              <h3>{title}</h3>
              <p>{copy}</p>
              {i < 3 && <ArrowRight className="step-arrow" size={18} />}
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="features-section">
        <div className="section-heading-row">
          <div>
            <span className="section-label">A little more protection</span>
            <h2>Helpful on the field.<br /><em>Powerful behind the scenes.</em></h2>
          </div>
          <p>
            Good crop care is a series of small decisions. AgriRakshak brings the right signal closer, without making you learn a new language.
          </p>
        </div>

        <div className="feature-grid">
          {[
            [Leaf, "AI disease detection", "Spot possible issues before they spread.", "green", "/farmer/diagnose"],
            [CloudSun, "Weather risk alerts", "Know when heat, rain, or humidity may matter.", "blue", "/farmer/chat?intent=weather"],
            [Bot, "Agricultural assistant", "Ask questions in English or Hindi.", "amber", "/farmer/chat"],
            [HeartHandshake, "Expert assistance", "Send uncertain cases to a real officer.", "terracotta", "/farmer/chat"],
            [ShieldCheck, "Simple and private", "Your field photos stay yours.", "green", "/farmer"],
            [Map, "Disease monitoring", "Help officers see the wider picture.", "blue", "/officer"],
          ].map(([Icon, title, copy, color, linkUrl]) => {
            const FeatureIcon = Icon as any;
            return (
              <Link href={linkUrl as string} className="feature-card" key={title as string}>
                <div className={`feature-icon ${color}`}>
                  <FeatureIcon size={22} />
                </div>
                <h3>{title as string}</h3>
                <p>{copy as string}</p>
                <ChevronRight size={18} className="feature-chevron" />
              </Link>
            );
          })}
        </div>
      </section>

      {/* Crop Focus Section */}
      <section className="crop-section">
        <div>
          <span className="section-label">Starting with the crops you know</span>
          <h2>Built around your<br /><em>everyday field.</em></h2>
          <p>We are beginning with rice and maize, and making it easy to add more crops as local knowledge grows.</p>
          <div className="crop-tags">
            <span>01 · Rice</span>
            <span>02 · Maize</span>
            <span className="muted">More crops soon</span>
          </div>
        </div>

        <div className="crop-card">
          <img src="/agrirakshak-rice-detail.jpg" alt="Rice leaf detail" />
          <div>
            <span>Field note / 014</span>
            <strong>Look closely.<br />Small changes matter.</strong>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="final-cta">
        <span className="section-label">Your next good decision</span>
        <h2>Have a crop problem?</h2>
        <p>Let AgriRakshak help you make sense of it.</p>
        <Link href="/farmer/diagnose" className="button button-paper">
          Scan your crop <ArrowRight size={18} />
        </Link>
      </section>

      {/* Footer */}
      <footer className="public-footer">
        <Brand />
        <span>Practical crop care, made clearer.</span>
        <span>© 2026 AgriRakshak · Smart India Hackathon</span>
      </footer>
    </div>
  );
}
