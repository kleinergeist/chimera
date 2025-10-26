import { Button } from "./ui/button";
import { Shield } from "./Icons";
import { SignInButton, SignUpButton } from '@clerk/clerk-react';

const Navigation = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-bold">Chimera</span>
          </div>
          
          <div className="flex items-center gap-4">
            <SignInButton mode="modal">
              <Button variant="ghost" size="sm">
                Sign In
              </Button>
            </SignInButton>
            <SignUpButton mode="modal">
              <Button size="sm" className="shadow-md">
                Get Started
              </Button>
            </SignUpButton>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

