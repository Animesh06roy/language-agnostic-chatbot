/**
 * ChatHeader — Top bar of the chatbot UI
 * Shows: project title, hackathon info, clear button
 */

interface Props {
  onClear: () => void;
}

export function ChatHeader({ onClear }: Props) {
  return (
    <div className="bg-slate-800 text-white px-5 py-4 flex items-center justify-between flex-shrink-0">
      {/* Left: Logo + Title */}
      <div className="flex items-center gap-3">
        {/* Bot icon */}
        <div className="w-10 h-10 rounded-xl bg-indigo-500 flex items-center justify-center flex-shrink-0">
          <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="8" width="18" height="13" rx="2" />
            <path d="M9 8V5a3 3 0 0 1 6 0v3" />
            <circle cx="9" cy="14" r="1.5" fill="currentColor" />
            <circle cx="15" cy="14" r="1.5" fill="currentColor" />
            <path d="M9 18h6" strokeLinecap="round" />
          </svg>
        </div>

        <div>
          <h1 className="font-semibold text-base leading-tight">
            Language Agnostic AI Chatbot
          </h1>
          <p className="text-slate-400 text-xs">
            Smart India Hackathon 2025 · PS-25104 · Smart Education
          </p>
        </div>
      </div>

      {/* Right: Status indicator + Clear button */}
      <div className="flex items-center gap-3">
        {/* Online indicator */}
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="hidden sm:inline">Online</span>
        </div>

        {/* Clear chat button */}
        <button
          onClick={onClear}
          className="text-xs text-slate-400 hover:text-white px-3 py-1.5 rounded-lg hover:bg-slate-700 transition-colors"
          title="Clear chat history"
        >
          Clear
        </button>
      </div>
    </div>
  );
}
