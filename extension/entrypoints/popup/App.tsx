import { useState, useEffect } from 'react';
import { CaptureButton } from '@/components/CaptureButton';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { Terminal, Zap, Copy, Check, Chrome } from 'lucide-react';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [captureId, setCaptureId] = useState('');
  const [copiedButton, setCopiedButton] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    // Listen for capture completion messages from content script
    const handleMessage = (message: any) => {
      if (message.action === 'captureCompleted') {
        setCaptureId(message.captureId);
        setShowSuccess(true);
      }
    };
    
    browser.runtime.onMessage.addListener(handleMessage);
    
    return () => {
      browser.runtime.onMessage.removeListener(handleMessage);
    };
  }, []);

  const handleCapture = async (type: 'component' | 'fullpage') => {
    setIsLoading(true);
    
    try {
      // Get the active tab
      const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
      
      if (!tab.id) {
        throw new Error('No active tab found');
      }

      // Check if we can access the tab
      if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) {
        throw new Error('Cannot capture on this page. Please navigate to a regular website.');
      }

      // Try to send message to content script with timeout
      try {
        const response = await Promise.race([
          browser.tabs.sendMessage(tab.id, {
            action: 'startCapture',
            type: type
          }),
          new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Timeout')), 3000)
          )
        ]);
        
        // If successful, close popup
        window.close();
      } catch (error) {
        console.log('Content script not available, trying to inject...');
        setIsRefreshing(true);
        
        // Try to inject the content script manually
        try {
          await browser.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content-scripts/content.js']
          });
          
          // Wait a moment for the script to initialize
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Try to send the capture message again
          await browser.tabs.sendMessage(tab.id, {
            action: 'startCapture',
            type: type
          });
          
          // If successful, close popup
          window.close();
        } catch (injectError) {
          console.error('Failed to inject content script:', injectError);
          throw new Error('Unable to inject capture functionality. Please refresh the page and try again.');
        }
      }
    } catch (error) {
      console.error('Error starting capture:', error);
      alert(`Capture failed: ${error.message}`);
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const copyToClipboard = async (text: string, buttonType: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedButton(buttonType);
      setTimeout(() => setCopiedButton(null), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  const CopyButton = ({ 
    text, 
    buttonType, 
    label 
  }: { 
    text: string; 
    buttonType: string; 
    label: string; 
  }) => {
    const isCopied = copiedButton === buttonType;
    
    return (
      <button
        onClick={() => copyToClipboard(text, buttonType)}
        className={`flex-1 px-3 py-2 text-xs font-medium rounded-md transition-all duration-200 flex items-center justify-center gap-2 ${
          isCopied
            ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-300'
            : 'bg-zinc-800/50 border border-zinc-700 text-zinc-300 hover:bg-zinc-700/50 hover:border-zinc-600'
        }`}
      >
        {isCopied ? (
          <>
            <Check className="w-3 h-3" />
            Copied!
          </>
        ) : (
          <>
            <Copy className="w-3 h-3" />
            {label}
          </>
        )}
      </button>
    );
  };

  return (
    <div className="w-80 h-auto bg-zinc-900 border border-zinc-800 rounded-lg shadow-2xl overflow-hidden">
      <div className="p-6 space-y-6">
        {/* Success State */}
        {showSuccess && (
          <div className="text-center space-y-4">
            <div className="w-12 h-12 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto">
              <Check className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-zinc-100 mb-2">
                Capture Complete!
              </h3>
              <p className="text-sm text-zinc-400">
                Your component has been captured and is ready to use.
              </p>
            </div>
            <div className="flex gap-2">
              <CopyButton
                text={`Capture ID: ${captureId}`}
                buttonType="capture-id"
                label="Copy ID"
              />
            </div>
          </div>
        )}

        {/* Main Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3">
            <h1 className="text-xl font-semibold text-zinc-100 tracking-tight">
              Web to MCP
            </h1>
          </div>
          
          {/* Description */}
          <p className="text-sm text-zinc-400 leading-relaxed">
            Select any website element and ship it straight to your coding assistant as a pixel‑perfect visual reference.
          </p>
        </div>

        {/* Capture Buttons - No Authentication Required */}
        <div className="space-y-4">
          {/* Component Capture Button */}
          <div className="power-up">
            <CaptureButton
              type="component"
              onClick={() => handleCapture('component')}
              disabled={isLoading}
              loading={isLoading}
            />
          </div>
          
          {/* Full Page Capture Button */}
          <div className="power-up">
            <CaptureButton
              type="fullpage"
              onClick={() => handleCapture('fullpage')}
              disabled={isLoading}
              loading={isLoading}
            />
          </div>
        </div>

        {/* Demo Mode Notice */}
        <div className="mt-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg">
          <div className="text-center">
            <div className="text-xs text-amber-400 font-medium">
              Demo Mode - No Authentication Required
            </div>
            <div className="text-xs text-amber-300 mt-1">
              Extension works directly without login
            </div>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex flex-col items-center gap-3 py-4 border border-zinc-800 bg-zinc-900/40 rounded-lg">
            <LoadingSpinner size="lg" />
            <div className="text-center space-y-1">
              {isRefreshing ? (
                <>
                  <p className="text-sm text-zinc-400 font-medium">
                    Refreshing page...
                  </p>
                </>
              ) : (
                <>
                  <p className="text-sm text-zinc-400 font-medium">
                    Initializing capture sequence...
                  </p>
                </>
              )}
            </div>
          </div>
        )}

        {/* Demo Mode - MCP features disabled */}
        <div className="pt-3 border-t border-zinc-800/60">
          <div className="text-center">
            <div className="text-xs text-zinc-500 font-medium">
              Demo Mode - MCP features disabled
            </div>
            <div className="text-xs text-zinc-600 mt-1">
              Extension works for component capture only
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;