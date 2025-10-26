import { useEffect, useState } from "react";

const nicknames = [
  "CutiePie2003",
  "GamerKing777",
  "TechWizard_42",
  "Anonymous123",
  "NightOwl2024",
  "CryptoNinja",
  "PixelMaster"
];

const websites = [
  "your portfolio",
  "LinkedIn",
  "Instagram",
  "Reddit",
  "Twitter",
  "Discord",
  "GitHub",
  "Facebook"
];

const RollingText = () => {
  const [nicknameIndex, setNicknameIndex] = useState(0);
  const [websiteIndex, setWebsiteIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setNicknameIndex((prev) => (prev + 1) % nicknames.length);
      setWebsiteIndex((prev) => (prev + 1) % websites.length);
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="py-8">
      <div className="max-w-4xl mx-auto text-center space-y-6">
          <p className="text-2xl md:text-3xl lg:text-4xl text-muted-foreground leading-relaxed">
            because{" "}
            <span className="relative inline-block">
              <span
                key={nicknameIndex}
                className="inline-block animate-fade-up font-semibold bg-gradient-hero bg-clip-text text-transparent"
              >
                {nicknames[nicknameIndex]}
              </span>
            </span>{" "}
            doesn't need to be on{" "}
            <span className="relative inline-block">
              <span
                key={websiteIndex}
                className="inline-block animate-fade-up font-semibold text-primary"
              >
                {websites[websiteIndex]}
              </span>
            </span>
          </p>
          
          <div className="flex items-center justify-center gap-8 pt-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-muted-foreground">Secure</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-blue-500" />
              <span className="text-muted-foreground">Fast</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-purple-500" />
              <span className="text-muted-foreground">Intuitive</span>
            </div>
          </div>
        </div>
    </div>
  );
};

export default RollingText;
