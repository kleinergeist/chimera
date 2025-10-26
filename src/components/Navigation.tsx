import { Button } from "@/components/ui/button";
import { Shield } from "lucide-react";

const Navigation = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">Chimera</span>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm">
              Sign In
            </Button>
            <Button size="sm" className="shadow-soft">
              Get Started
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
