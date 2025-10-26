import { Button } from "./ui/button";
import { Shield } from "./Icons";
import RollingText from "./RollingText";

const Hero = ({ onGetStarted }) => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-b from-white via-blue-50 to-purple-50">
      <div className="absolute inset-0 bg-gradient-to-b from-blue-600/5 via-transparent to-transparent" />
      
      <div className="container mx-auto px-4 py-32 relative z-10">
        <div className="grid lg:grid-cols-1 gap-12 items-center">
          <div className="space-y-10 animate-fade-in text-center pb-12">
            <div className="flex flex-wrap gap-3 justify-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 rounded-full border border-blue-200">
                <Shield className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">Personal Cyber Security</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 rounded-full border border-purple-200">
                <span className="text-sm font-medium text-gray-900">Cybersecurity Awareness Month 2025</span>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight">
              Protect Your
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Digital Identity
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 max-w-xl mx-auto">
              One you. Many faces. Zero regrets.
            </p>
            
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 rounded-full border border-purple-200">
              <span className="text-sm font-medium text-gray-900">Hackathon Prototype Demo</span>
            </div>
            
            <RollingText />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

