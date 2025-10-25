import React, { useState, useRef, useEffect } from 'react';
import { Button } from './button';
import { Chrome, Download, ExternalLink, ChevronDown, Terminal } from 'lucide-react';
import { cn } from '~/lib/utils';

interface AddToChromeDropdownProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export const AddToChromeDropdown: React.FC<AddToChromeDropdownProps> = ({ className, ...props }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleDownloadExtension = async () => {
    try {
      const button = document.querySelector('[data-download-button]') as HTMLButtonElement;
      if (button) {
        button.disabled = true;
        button.textContent = 'Downloading...';
      }

      // Create a download link for the extension zip
      const response = await fetch('http://localhost:8000/api/extension/download/'); // Fixed URL
      
      if (response.ok) {
        const blob = await response.blob();
        
        if (blob.size > 0 && blob.type === 'application/zip') {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'web-to-mcp-extension.zip';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
          
          alert('Extension downloaded successfully! Extract the zip file and load it as an unpacked extension in Chrome.');
        } else {
          throw new Error('Invalid file received');
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Server error: ${response.status}`);
      }
    } catch (error) {
      console.error('Error downloading extension:', error);
      
      const errorMessage = error instanceof Error ? error.message : 'Download failed';
      alert(`Extension download failed: ${errorMessage}\n\nRedirecting to Chrome Web Store instead...`);
      
      setTimeout(() => {
        window.open("https://chromewebstore.google.com/detail/web-to-mcp/hbnhkfkblpgjlfonnikijlofeiabolmi", "_blank");
      }, 1000);
    } finally {
      const button = document.querySelector('[data-download-button]') as HTMLButtonElement;
      if (button) {
        button.disabled = false;
        button.textContent = 'Download Extension';
      }
    }
    setIsOpen(false);
  };

  const handleChromeWebStore = () => {
    window.open("https://chromewebstore.google.com/detail/web-to-mcp/hbnhkfkblpgjlfonnikijlofeiabolmi", "_blank");
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
          "bg-emerald-500 hover:bg-emerald-400 text-zinc-900 font-semibold",
          className
        )}
        onClick={() => setIsOpen(!isOpen)}
        {...props}
      >
        Add to Chrome <ChevronDown className="ml-2 h-4 w-4" />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-64 bg-zinc-900 border border-zinc-800 rounded-lg shadow-lg z-50">
          <div className="py-2">
            <button
              className="w-full px-4 py-3 text-left hover:bg-zinc-800 transition-colors flex items-center"
              onClick={handleDownloadExtension}
              data-download-button
            >
              <Download className="h-5 w-5 mr-3 text-emerald-400" />
              <div>
                <div className="font-medium text-zinc-200">Download Extension</div>
                <div className="text-sm text-zinc-400">Get the .zip file to install manually</div>
              </div>
            </button>
            <button
              className="w-full px-4 py-3 text-left hover:bg-zinc-800 transition-colors flex items-center"
              onClick={handleChromeWebStore}
            >
              <Chrome className="h-5 w-5 mr-3 text-blue-400" />
              <div>
                <div className="font-medium text-zinc-200">Chrome Web Store</div>
                <div className="text-sm text-zinc-400">Install directly from the Chrome Web Store</div>
              </div>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};