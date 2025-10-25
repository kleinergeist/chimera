import { SignIn, SignUp } from '@clerk/clerk-react';
import { useState } from 'react';

function LandingPage() {
  const [showSignUp, setShowSignUp] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Hero content */}
        <div className="text-center md:text-left space-y-6">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Chimera
          </h1>
          <p className="text-2xl text-gray-700">
            Discover, organize, and manage your digital accounts
          </p>
          <p className="text-lg text-gray-600">
            A modern platform for account discovery and intelligent categorization
          </p>
          <div className="flex gap-4 justify-center md:justify-start">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Secure</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Fast</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Intuitive</span>
            </div>
          </div>
        </div>

        {/* Right side - Auth */}
        <div className="flex justify-center">
          <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
            {!showSignUp ? (
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-gray-800 text-center">Welcome Back</h2>
                <SignIn 
                  appearance={{
                    elements: {
                      rootBox: "w-full",
                      card: "shadow-none"
                    }
                  }}
                />
                <p className="text-center text-sm text-gray-600">
                  Don't have an account?{' '}
                  <button 
                    onClick={() => setShowSignUp(true)}
                    className="text-blue-600 hover:text-blue-700 font-semibold"
                  >
                    Sign up
                  </button>
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-gray-800 text-center">Create Account</h2>
                <SignUp 
                  appearance={{
                    elements: {
                      rootBox: "w-full",
                      card: "shadow-none"
                    }
                  }}
                />
                <p className="text-center text-sm text-gray-600">
                  Already have an account?{' '}
                  <button 
                    onClick={() => setShowSignUp(false)}
                    className="text-blue-600 hover:text-blue-700 font-semibold"
                  >
                    Sign in
                  </button>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;

