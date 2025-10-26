import { UserCheck, Search, Eye } from "./Icons";
import { Card, CardContent } from "./ui/card";

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
    icon: Eye,
    title: "Visibility Control",
    description: "Choose exactly what information you want to share and with whom.",
  },
];

const Features = () => {
  return (
    <section className="py-24 bg-gradient-to-b from-white via-blue-50 to-white">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold">
            Complete Cyber Security Suite
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Everything you need to protect your digital identity and maintain privacy online.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="border-gray-200 hover:border-blue-300 transition-all duration-300 hover:shadow-lg animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <CardContent className="p-6 space-y-4">
                <div className="h-14 w-14 rounded-lg bg-blue-100 flex items-center justify-center p-3">
                  <feature.icon className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;

