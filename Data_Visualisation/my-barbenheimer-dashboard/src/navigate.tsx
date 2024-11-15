'use client'

import { useState } from 'react';

import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Explore top movies', href: '#' }, // This will trigger the navigation to App
  { name: 'Education', href: 'education' },
  { name: 'Marketplace', href: '#' },
  { name: 'Company', href: '#' },
];

export default function Navigate({ switchToApp, switchToEdu, switchToPro }: { switchToApp: () => void;  switchToEdu: () => void; switchToPro: () => void }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="bg-white" 
      style={{
        backgroundColor: 'black',
        backgroundImage: "url('https://as2.ftcdn.net/v2/jpg/09/57/95/07/1000_F_957950798_xL7qEhuj023sj4Jz30rgCW7ZmxGaItqv.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        minHeight: '110vh',
        height: '100vh',      // Sets the height to full viewport height
        width: '150%',        // Ensures it covers full width
        overflow: 'hidden'

      }}
      >
      <header className="absolute inset-x-0 top-0 z-50">
        <nav aria-label="Global" className="flex items-center justify-between p-6 lg:px-8">
          <div className="flex lg:flex-1">
            <a href="#" className="-m-1.5 p-1.5">
              <span className="sr-only">NandetechAI</span>
              {/* <img
                alt=""
                src="https://hanjoes.github.io/blog/images/data-vis-gb-header.jpg"
                className="h-20 w-auto"
              /> */}
            </a>
          </div>
          <div className="flex lg:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon aria-hidden="true" className="h-6 w-6" />
            </button>
          </div>
          <div className="hidden lg:flex lg:gap-x-14">
          {navigation.map((item) => (
            <a
              key={item.name}
              href="#"
              onClick={() => {
                if (item.name === 'Explore top movies') {
                  switchToApp(); // Action for 'Explore top movies'
                } else if (item.name === 'Education') {
                  switchToEdu();
                  
                } else if (item.name === 'Marketplace') {
                  switchToPro();
                }
              }}
              className="text-sm font-semibold text-gray-900"
            >
              {item.name}
            </a>
          ))}
        </div>

        </nav>
      </header>

      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-5xl font-semibold tracking-tight text-gray-900 sm:text-7xl">
              Data is storytelling
            </h1>
            <p className="mt-8 text-lg font-medium text-black-1000 sm:text-xl">
            Data visualization transforms complex information into clear, 
            engaging visuals, making it easier to uncover insights,
            tell compelling stories, and feel empowered by data at a glance.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <a
                href="#"
                onClick={switchToApp} // This button also switches to App
                className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Get started
              </a>
              <a href="#" className="text-sm font-semibold text-gray-900">
                Learn more <span aria-hidden="true">→</span>
              </a>
            </div>
          </div>
        </div>
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
          />
        </div>
      </div>
      </div>
    
  );
}
