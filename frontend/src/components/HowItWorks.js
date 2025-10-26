import { CheckCircle2 } from "./Icons";

const steps = [
  {
    number: "01",
    title: "Sign Up & Scan",
    description: "Create your account and run your first digital footprint scan. We'll analyze your online presence across the web.",
  },
  {
    number: "02",
    title: "Review Results",
    description: "Get a detailed report of your digital footprint, including exposed data, public records, and potential vulnerabilities.",
  },
  {
    number: "03",
    title: "Create Personas",
    description: "Set up separate online identities for different aspects of your life - work, personal, hobbies, and more.",
  },
];

const HowItWorks = () => {
  return (
    <section className="py-24 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold">
            How Chimera Works
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get started with complete digital protection in three simple steps.
          </p>
        </div>
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-5xl mx-auto">
          {steps.map((step, index) => (
            <div 
              key={index} 
              className="flex gap-6 animate-fade-in"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="flex-shrink-0">
                <div className="h-16 w-16 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                  {step.number}
                </div>
              </div>
              <div className="space-y-3 pt-1">
                <h3 className="text-2xl font-semibold flex items-center gap-2">
                  {step.title}
                  <CheckCircle2 className="h-5 w-5 text-blue-600" />
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;

