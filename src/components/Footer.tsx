import { Shield } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border bg-background">
      <div className="container mx-auto px-4">
        <div className="flex justify-center mb-8">
          <div className="space-y-4 text-center">
            <div className="flex items-center gap-2">
              <Shield className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold">Chimera</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Protecting your digital identity with advanced security and privacy tools.
            </p>
          </div>
        </div>
        
        <div className="pt-8 border-t border-border text-center">
          <p className="text-sm text-muted-foreground">
            © 2025 Chimera. Hackathon Prototype Demo.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
