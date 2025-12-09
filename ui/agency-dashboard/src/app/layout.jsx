import './globals.css';

export const metadata = {
  title: 'Agency Swarm Command',
  description: 'Multi-Agent AI Control Dashboard',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-cyber-black min-h-screen grid-bg">
        {children}
      </body>
    </html>
  );
}
