import { Shield, UserCheck, Search, Lock, Eye, Fingerprint } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: UserCheck,
    title: "Persona Management",
    description: "Create and manage multiple online identities to keep your personal and professional lives separate.",
  },
  {
    icon: Search,
    title: "Digital Footprint Scan",
    description: "Discover what information about you is publicly available and take action to protect it.",
  },
  {
    icon: Shield,
    title: "Real-time Monitoring",
    description: "Get instant alerts when your personal information appears in data breaches or leaks.",
  },
  {
    icon: Lock,
    title: "Privacy Protection",
    description: "Advanced encryption and security measures to keep your data safe from prying eyes.",
  },
  {
    icon: Eye,
    title: "Visibility Control",
    description: "Choose exactly what information you want to share and with whom.",
  },
  {
    icon: Fingerprint,
    title: "Identity Verification",
    description: "Secure authentication methods to prove you are who you say you are.",
  },
];

const Features = () => {
  return (
    <section className="py-24 bg-gradient-feature">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-16 animate-fade-up">
          <h2 className="text-4xl md:text-5xl font-bold">
            Complete Cyber Security Suite
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Everything you need to protect your digital identity and maintain privacy online.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="border-border/50 hover:border-primary/50 transition-all duration-300 hover:shadow-soft animate-fade-up"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <CardContent className="p-6 space-y-4">
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
