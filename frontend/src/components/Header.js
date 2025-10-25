import { UserButton } from '@clerk/clerk-react';

function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Chimera
          </h1>
          <div className="flex items-center gap-4">
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

