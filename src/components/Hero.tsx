import { Button } from "@/components/ui/button";
import { Shield, ArrowRight } from "lucide-react";
import heroImage from "@/assets/hero-security.jpg";
import RollingText from "./RollingText";

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-feature">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
      
      <div className="container mx-auto px-4 py-32 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-10 animate-fade-up pb-12">
            <div className="flex flex-wrap gap-3">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full border border-primary/20">
                <Shield className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium text-foreground">Personal Cyber Security</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 rounded-full border border-accent/20">
                <span className="text-sm font-medium text-foreground">Cybersecurity Awareness Month 2025</span>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight">
              Protect Your
              <span className="block bg-gradient-hero bg-clip-text text-transparent">
                Digital Identity
              </span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-xl">
              One you. Many faces. Zero regrets.
            </p>
            
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 rounded-full border border-accent/20">
              <span className="text-sm font-medium text-foreground">Hackathon Prototype Demo</span>
            </div>
            
            <RollingText />
            </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
