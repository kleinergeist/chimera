import Navigation from '../components/Navigation';
import Hero from '../components/Hero';
import Features from '../components/Features';
import HowItWorks from '../components/HowItWorks';
import CTA from '../components/CTA';
import Footer from '../components/Footer';
import { useClerk } from '@clerk/clerk-react';

function NewLandingPage() {
  const { openSignUp } = useClerk();

  const handleGetStarted = () => {
    openSignUp();
  };

  return (
    <div className="min-h-screen bg-white">
      <Navigation />
      <Hero onGetStarted={handleGetStarted} />
      <Features />
      <HowItWorks />
      <CTA onGetStarted={handleGetStarted} />
      <Footer />
    </div>
  );
}

export default NewLandingPage;

