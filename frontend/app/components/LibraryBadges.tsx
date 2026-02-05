'use client';

import { useMemo } from 'react';

interface LibraryBadgesProps {
    code: string;
}

const LIBRARY_COLORS: Record<string, string> = {
    pandas: 'bg-blue-600',
    numpy: 'bg-orange-600',
    scipy: 'bg-purple-600',
    sklearn: 'bg-green-600',
    tensorflow: 'bg-yellow-600',
    torch: 'bg-red-600',
    requests: 'bg-cyan-600',
    flask: 'bg-gray-600',
    django: 'bg-emerald-600',
    matplotlib: 'bg-pink-600',
};

export default function LibraryBadges({ code }: LibraryBadgesProps) {
    const detectedLibraries = useMemo(() => {
        const libraries: string[] = [];

        // Regex to match import statements
        const importRegex = /(?:import|from)\s+(\w+)/g;
        let match;

        while ((match = importRegex.exec(code)) !== null) {
            const lib = match[1].toLowerCase();
            if (!libraries.includes(lib) && lib !== 'os' && lib !== 'sys' && lib !== 'json') {
                libraries.push(lib);
            }
        }

        return libraries.slice(0, 5); // Limit to 5 badges
    }, [code]);

    if (detectedLibraries.length === 0) {
        return null;
    }

    return (
        <div className="flex flex-wrap gap-2">
            {detectedLibraries.map((lib) => (
                <span
                    key={lib}
                    className={`px-2 py-1 rounded-full text-xs font-medium text-white ${LIBRARY_COLORS[lib] || 'bg-gray-500'
                        }`}
                >
                    {lib.charAt(0).toUpperCase() + lib.slice(1)}
                </span>
            ))}
        </div>
    );
}
