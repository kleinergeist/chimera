import { SignIn, SignUp } from '@clerk/clerk-react';
import { useState } from 'react';

function LandingPage() {
  const [showSignUp, setShowSignUp] = useState(false);

  const nicknames = ['lovergirl69', 'xXDarkLord420Xx', 'CutiePie2003', 'MemeLord9000', 'GamerBoi'];
  const websites = ['LinkedIn', 'Facebook', 'your portfolio', 'Instagram', 'Twitter'];

  // Create triple array for seamless infinite scroll
  const infiniteNicknames = [...nicknames, ...nicknames, ...nicknames];
  const infiniteWebsites = [...websites, ...websites, ...websites];

  const nicknameAnimationDuration = nicknames.length * 3; // 3 seconds per item
  const websiteAnimationDuration = websites.length * 3;

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Hero content */}
        <div className="text-center md:text-left space-y-6">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Chimera
          </h1>
          <p className="text-2xl text-gray-700">
One you. Many faces. Zero regrets.          </p>
          <p className="text-lg text-gray-600">
Online persona management made easy. <br />
Because your digital foorprint matters.          </p>
          <p className="text-base text-gray-500 italic flex flex-wrap items-center justify-center md:justify-start">
            <span className="whitespace-nowrap">because&nbsp;</span>
            <span className="font-semibold text-purple-600 inline-block overflow-hidden h-6 relative" style={{ width: '180px' }}>
              <style>{`
                @keyframes scrollNicknames {
                  ${infiniteNicknames.map((_, idx) => {
                    const percent = (idx / nicknames.length) * 100;
                    const nextPercent = ((idx + 0.3) / nicknames.length) * 100;
                    return `
                      ${percent}% { transform: translateY(-${idx * 24}px); }
                      ${nextPercent}% { transform: translateY(-${(idx + 1) * 24}px); }
                      ${((idx + 1) / nicknames.length) * 100}% { transform: translateY(-${(idx + 1) * 24}px); }
                    `;
                  }).join('')}
                }
              `}</style>
              <span 
                className="absolute"
                style={{ 
                  display: 'flex',
                  flexDirection: 'column',
                  animation: `scrollNicknames ${nicknameAnimationDuration}s ease-in-out infinite`
                }}
              >
                {infiniteNicknames.map((nickname, idx) => (
                  <span key={idx} className="h-6 leading-6">{nickname}</span>
                ))}
              </span>
            </span>
            <span className="whitespace-nowrap">&nbsp;doesn't need to be on&nbsp;</span>
            <span className="font-semibold text-blue-600 inline-block overflow-hidden h-6 relative" style={{ width: '120px' }}>
              <style>{`
                @keyframes scrollWebsites {
                  ${infiniteWebsites.map((_, idx) => {
                    const percent = (idx / websites.length) * 100;
                    const nextPercent = ((idx + 0.3) / websites.length) * 100;
                    return `
                      ${percent}% { transform: translateY(-${idx * 24}px); }
                      ${nextPercent}% { transform: translateY(-${(idx + 1) * 24}px); }
                      ${((idx + 1) / websites.length) * 100}% { transform: translateY(-${(idx + 1) * 24}px); }
                    `;
                  }).join('')}
                }
              `}</style>
              <span 
                className="absolute"
                style={{ 
                  display: 'flex',
                  flexDirection: 'column',
                  animation: `scrollWebsites ${websiteAnimationDuration}s ease-in-out infinite`
                }}
              >
                {infiniteWebsites.map((website, idx) => (
                  <span key={idx} className="h-6 leading-6">{website}</span>
                ))}
              </span>
            </span>
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
          <div className="max-w-sm w-full">
            {!showSignUp ? (
              <SignIn 
                appearance={{
                  elements: {
                    rootBox: "w-full",
                    card: "shadow-md w-full mx-auto",
                    headerTitle: "text-center",
                    headerSubtitle: "text-center",
                    socialButtonsBlockButton: "justify-center",
                    formButtonPrimary: "w-full",
                    formFieldInput: "w-full",
                    footer: "text-center",
                    footerAction: "text-center justify-center",
                    footerActionText: "text-center",
                    footerActionLink: "text-center",
                    identityPreview: "w-full",
                    formFieldRow: "w-full"
                  }
                }}
              />
            ) : (
              <SignUp 
                appearance={{
                  elements: {
                    rootBox: "w-full",
                    card: "shadow-md w-full mx-auto",
                    headerTitle: "text-center",
                    headerSubtitle: "text-center",
                    socialButtonsBlockButton: "justify-center",
                    formButtonPrimary: "w-full",
                    formFieldInput: "w-full",
                    footer: "text-center",
                    footerAction: "text-center justify-center",
                    footerActionText: "text-center",
                    footerActionLink: "text-center",
                    identityPreview: "w-full",
                    formFieldRow: "w-full"
                  }
                }}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;

