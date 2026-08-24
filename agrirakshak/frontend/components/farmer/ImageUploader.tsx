"use client";

import React, { useState, useRef } from "react";
import { Camera, Upload, X, Image as ImageIcon, Loader2 } from "lucide-react";

interface ImageUploaderProps {
  onImageSelected: (base64: string) => void;
  isLoading?: boolean;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onImageSelected,
  isLoading = false,
}) => {
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        alert("Please upload a valid image file (JPEG, PNG, WEBP).");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        alert("Image file size must be less than 10MB.");
        return;
      }

      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result as string;
        setPreview(base64);
        onImageSelected(base64);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemove = () => {
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    if (cameraInputRef.current) cameraInputRef.current.value = "";
  };

  return (
    <div className="w-full bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
      <h3 className="text-base font-semibold text-gray-800 mb-3 flex items-center gap-2">
        <Camera className="w-5 h-5 text-agri-600" />
        Scan Affected Leaf
      </h3>

      {preview ? (
        <div className="relative rounded-xl overflow-hidden border border-agri-200 bg-gray-50">
          <img
            src={preview}
            alt="Uploaded Leaf Preview"
            className="w-full h-48 object-cover rounded-xl"
          />
          <button
            onClick={handleRemove}
            className="absolute top-2 right-2 bg-red-500 text-white p-1.5 rounded-full shadow hover:bg-red-600 transition"
          >
            <X className="w-4 h-4" />
          </button>
          {isLoading && (
            <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex flex-col items-center justify-center text-white">
              <Loader2 className="w-8 h-8 animate-spin mb-2" />
              <span className="text-sm font-medium">Analyzing your crop leaf...</span>
            </div>
          )}
        </div>
      ) : (
        <div className="border-2 border-dashed border-agri-200 rounded-xl p-6 flex flex-col items-center justify-center bg-agri-50/50 hover:bg-agri-50 transition cursor-pointer">
          <ImageIcon className="w-10 h-10 text-agri-500 mb-2" />
          <p className="text-sm font-medium text-gray-700 text-center">
            Upload clear photo of affected leaf
          </p>
          <p className="text-xs text-gray-400 mt-1 mb-4 text-center">
            Supports JPEG, PNG, WEBP (Max 10MB)
          </p>

          <div className="flex gap-3 w-full max-w-xs">
            <button
              onClick={() => cameraInputRef.current?.click()}
              className="flex-1 bg-agri-600 hover:bg-agri-700 text-white text-xs font-semibold py-2.5 px-3 rounded-lg flex items-center justify-center gap-1.5 shadow-sm transition"
            >
              <Camera className="w-4 h-4" />
              Camera
            </button>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex-1 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 text-xs font-semibold py-2.5 px-3 rounded-lg flex items-center justify-center gap-1.5 shadow-sm transition"
            >
              <Upload className="w-4 h-4" />
              Gallery
            </button>
          </div>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/jpeg,image/png,image/webp"
            className="hidden"
          />
          <input
            type="file"
            ref={cameraInputRef}
            onChange={handleFileChange}
            accept="image/*"
            capture="environment"
            className="hidden"
          />
        </div>
      )}
    </div>
  );
};
