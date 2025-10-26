import { Button } from "@/components/ui/button";
import { ArrowRight, Shield } from "lucide-react";

const CTA = () => {
  return (
    <section className="py-24 bg-gradient-feature">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="relative rounded-3xl overflow-hidden shadow-glow">
            <div className="absolute inset-0 bg-gradient-hero opacity-95" />
            
            <div className="relative z-10 px-8 py-16 md:px-16 md:py-20 text-center space-y-8">
              <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-white/20 backdrop-blur-sm mb-4">
                <Shield className="h-8 w-8 text-white" />
              </div>
              
              <h2 className="text-4xl md:text-5xl font-bold text-white">
                Interested in the Concept?
              </h2>
              
              <p className="text-xl text-white/90 max-w-2xl mx-auto">
                This is a prototype demonstration showcasing how persona management
                can help protect your digital identity and privacy.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <Button 
                  size="lg" 
                  variant="secondary"
                  className="group"
                >
                  View Demo
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
                <Button 
                  size="lg" 
                  variant="outline"
                  className="bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-sm"
                >
                  Learn More
                </Button>
              </div>
              
              <p className="text-sm text-white/70">
                Built for hackathon demonstration purposes
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
