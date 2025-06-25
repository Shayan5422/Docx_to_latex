'use client';

import { useState, useRef } from 'react';
import { Upload, FileText, Download, Settings, HelpCircle, Sparkles, Zap, Check, X, Loader } from 'lucide-react';

interface ConversionOptions {
  generateToc: boolean;
  overleafCompatible: boolean;
  preserveStyles: boolean;
  preserveLineBreaks: boolean;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [outputFileName, setOutputFileName] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [conversionComplete, setConversionComplete] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [options, setOptions] = useState<ConversionOptions>({
    generateToc: false,
    overleafCompatible: true,
    preserveStyles: true,
    preserveLineBreaks: true,
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setOutputFileName(file.name.replace('.docx', '.tex'));
      setConversionComplete(false);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file && file.name.endsWith('.docx')) {
      setSelectedFile(file);
      setOutputFileName(file.name.replace('.docx', '.tex'));
      setConversionComplete(false);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleConvert = async () => {
    if (!selectedFile) return;
    
    setIsConverting(true);
    
    try {
      // First, upload the file
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      const uploadResponse = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!uploadResponse.ok) {
        throw new Error('File upload failed');
      }
      
      const uploadData = await uploadResponse.json();
      const taskId = uploadData.task_id;
      
      // Then, start the conversion
      const convertResponse = await fetch('http://localhost:5000/api/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_id: taskId,
          output_filename: outputFileName,
          options: {
            generateToc: options.generateToc,
            overleafCompatible: options.overleafCompatible,
            preserveStyles: options.preserveStyles,
            preserveLineBreaks: options.preserveLineBreaks,
            extractMedia: true,
          },
        }),
      });
      
      if (!convertResponse.ok) {
        throw new Error('Conversion failed');
      }
      
      const convertData = await convertResponse.json();
      
      // Store task ID for download
      setTaskId(taskId);
      setIsConverting(false);
      setConversionComplete(true);
      
    } catch (error) {
      console.error('Conversion error:', error);
      setIsConverting(false);
      // You might want to show an error state here
    }
  };

  const toggleOption = (key: keyof ConversionOptions) => {
    setOptions(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-4 rounded-2xl shadow-lg">
              <FileText className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
            DOCX to LaTeX Converter
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Transform your Word documents into beautiful LaTeX files with enhanced formatting and Overleaf compatibility
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Main Conversion Card */}
          <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-3xl shadow-2xl border border-white/20 p-8 mb-8">
            {/* File Upload Section */}
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6 flex items-center">
                <Upload className="w-6 h-6 mr-3 text-indigo-500" />
                Upload Your Document
              </h2>
              
              <div
                className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer ${
                  selectedFile 
                    ? 'border-green-300 bg-green-50 dark:bg-green-900/20' 
                    : 'border-gray-300 hover:border-indigo-400 bg-gray-50/50 dark:bg-gray-700/50'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".docx"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                
                {selectedFile ? (
                  <div className="flex flex-col items-center">
                    <div className="bg-green-100 dark:bg-green-800 p-4 rounded-full mb-4">
                      <Check className="w-8 h-8 text-green-600 dark:text-green-300" />
                    </div>
                    <h3 className="text-lg font-semibold text-green-700 dark:text-green-300 mb-2">
                      File Selected
                    </h3>
                    <p className="text-green-600 dark:text-green-400 font-medium">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      Click to select a different file
                    </p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <div className="bg-indigo-100 dark:bg-indigo-800 p-4 rounded-full mb-4">
                      <Upload className="w-8 h-8 text-indigo-600 dark:text-indigo-300" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      Drop your DOCX file here
                    </h3>
                    <p className="text-gray-500 dark:text-gray-400">
                      or click to browse your files
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Output File Name */}
            {selectedFile && (
              <div className="mb-8">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Output File Name
                </label>
                <input
                  type="text"
                  value={outputFileName}
                  onChange={(e) => setOutputFileName(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200"
                  placeholder="output.tex"
                />
              </div>
            )}

            {/* Advanced Options */}
            <div className="mb-8">
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="flex items-center text-lg font-semibold text-gray-800 dark:text-white mb-4 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
              >
                <Settings className="w-5 h-5 mr-2" />
                Advanced Options
                <span className={`ml-2 transition-transform duration-200 ${showAdvanced ? 'rotate-180' : ''}`}>
                  ↓
                </span>
              </button>

              {showAdvanced && (
                <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-6 space-y-4 animate-in slide-in-from-top-5 duration-300">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <label className="flex items-center space-x-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={options.generateToc}
                        onChange={() => toggleOption('generateToc')}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <span className="text-gray-700 dark:text-gray-300">
                        📑 Generate Table of Contents
                      </span>
                    </label>

                    <label className="flex items-center space-x-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={options.overleafCompatible}
                        onChange={() => toggleOption('overleafCompatible')}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <span className="text-blue-600 dark:text-blue-400">
                        🔧 Overleaf Compatible
                      </span>
                    </label>

                    <label className="flex items-center space-x-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={options.preserveStyles}
                        onChange={() => toggleOption('preserveStyles')}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <span className="text-green-600 dark:text-green-400">
                        🎨 Preserve Styles
                      </span>
                    </label>

                    <label className="flex items-center space-x-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={options.preserveLineBreaks}
                        onChange={() => toggleOption('preserveLineBreaks')}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <span className="text-purple-600 dark:text-purple-400">
                        📝 Preserve Line Breaks
                      </span>
                    </label>
                  </div>

                  <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-blue-600 dark:text-blue-400">
                      💡 <strong>Tip:</strong> Enhanced options are enabled by default for best results
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Convert Button */}
            <div className="text-center">
              <button
                onClick={handleConvert}
                disabled={!selectedFile || isConverting}
                className={`
                  inline-flex items-center px-8 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 transform
                  ${selectedFile && !isConverting
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl hover:scale-105'
                    : 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                  }
                `}
              >
                {isConverting ? (
                  <>
                    <Loader className="w-6 h-6 mr-3 animate-spin" />
                    Converting...
                  </>
                ) : conversionComplete ? (
                  <>
                    <Check className="w-6 h-6 mr-3" />
                    Converted Successfully!
                  </>
                ) : (
                  <>
                    <Zap className="w-6 h-6 mr-3" />
                    Convert to LaTeX
                  </>
                )}
              </button>
            </div>

            {/* Progress Indicator */}
            {isConverting && (
              <div className="mt-8 animate-in fade-in-50 duration-500">
                <div className="bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 h-full rounded-full animate-pulse w-2/3 transition-all duration-1000"></div>
                </div>
                <p className="text-center text-gray-600 dark:text-gray-400 mt-2">
                  Processing your document...
                </p>
              </div>
            )}

            {/* Download Section */}
            {conversionComplete && (
              <div className="mt-8 p-6 bg-green-50 dark:bg-green-900/20 rounded-2xl border border-green-200 dark:border-green-800 animate-in slide-in-from-bottom-5 duration-500">
                <div className="flex flex-col space-y-4">
                  <div className="flex items-center">
                    <div className="bg-green-100 dark:bg-green-800 p-3 rounded-full mr-4">
                      <Download className="w-6 h-6 text-green-600 dark:text-green-300" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-green-700 dark:text-green-300">
                        Conversion Complete!
                      </h3>
                      <p className="text-green-600 dark:text-green-400">
                        Your LaTeX files are ready for download
                      </p>
                    </div>
                  </div>
                  
                  {/* Download Options */}
                  <div className="flex flex-col sm:flex-row gap-3">
                    {/* LaTeX File Only */}
                    <button 
                      onClick={() => taskId && window.open(`http://localhost:5000/api/download/${taskId}`, '_blank')}
                      className="flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 hover:scale-105 transform"
                    >
                      <FileText className="w-5 h-5 mr-2" />
                      LaTeX File Only
                    </button>
                    
                    {/* Complete Package */}
                    <button 
                      onClick={() => taskId && window.open(`http://localhost:5000/api/download-complete/${taskId}`, '_blank')}
                      className="flex items-center justify-center bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 hover:scale-105 transform"
                    >
                      <Download className="w-5 h-5 mr-2" />
                      Complete Package (ZIP)
                    </button>
                  </div>
                  
                  {/* Download Description */}
                  <div className="text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 p-3 rounded-lg">
                    <p className="mb-1">
                      <strong>Complete package includes:</strong> LaTeX file + images + usage guide
                    </p>
                    <p className="text-xs text-gray-500">
                      Ready for Overleaf or local compilation
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Help Section */}
          <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-3xl shadow-2xl border border-white/20 p-8">
            <button
              onClick={() => setShowHelp(!showHelp)}
              className="flex items-center text-xl font-semibold text-gray-800 dark:text-white mb-4 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              <HelpCircle className="w-6 h-6 mr-3" />
              Enhancement Options Help
              <span className={`ml-2 transition-transform duration-200 ${showHelp ? 'rotate-180' : ''}`}>
                ↓
              </span>
            </button>

            {showHelp && (
              <div className="space-y-6 text-gray-600 dark:text-gray-300 animate-in slide-in-from-top-5 duration-300">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <h4 className="font-semibold text-blue-700 dark:text-blue-300 mb-2">
                      🔧 Overleaf Compatible
                    </h4>
                    <p className="text-sm">
                      Makes images work properly in Overleaf by converting absolute paths to relative paths. Essential for cloud LaTeX editors.
                    </p>
                  </div>

                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <h4 className="font-semibold text-green-700 dark:text-green-300 mb-2">
                      🎨 Preserve Styles
                    </h4>
                    <p className="text-sm">
                      Maintains document formatting, adds centering for figures and tables, and includes additional LaTeX packages for better formatting.
                    </p>
                  </div>

                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <h4 className="font-semibold text-purple-700 dark:text-purple-300 mb-2">
                      📝 Preserve Line Breaks
                    </h4>
                    <p className="text-sm">
                      Fixes numbered list display issues, maintains proper paragraph spacing, and prevents pagination problems.
                    </p>
                  </div>

                  <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                    <h4 className="font-semibold text-yellow-700 dark:text-yellow-300 mb-2">
                      📑 Table of Contents
                    </h4>
                    <p className="text-sm">
                      Automatically generates a table of contents based on your document's headings and structure.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12">
          <p className="text-gray-500 dark:text-gray-400">
            Enhanced DOCX to LaTeX Converter v2.0 | Built with Next.js & Tailwind CSS
          </p>
        </div>
      </div>

      {/* Custom CSS for animations */}
      <style jsx global>{`
        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
        @keyframes fade-in-50 {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes slide-in-from-top-5 {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes slide-in-from-bottom-5 {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-in {
          animation-duration: 300ms;
          animation-fill-mode: both;
        }
        .fade-in-50 {
          animation-name: fade-in-50;
        }
        .slide-in-from-top-5 {
          animation-name: slide-in-from-top-5;
        }
        .slide-in-from-bottom-5 {
          animation-name: slide-in-from-bottom-5;
        }
        .duration-300 {
          animation-duration: 300ms;
        }
        .duration-500 {
          animation-duration: 500ms;
        }
      `}</style>
    </div>
  );
}
