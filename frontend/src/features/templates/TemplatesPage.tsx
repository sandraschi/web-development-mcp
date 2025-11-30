import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Filter, FileText, RefreshCw, Star, Download, GitBranch } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

// Mock data - replace with actual API calls
const mockTemplates = [
  { 
    id: 'react-ts', 
    name: 'React + TypeScript', 
    description: 'A modern React project with TypeScript, Vite, and Tailwind CSS',
    category: 'react',
    stars: 1243,
    downloads: 5421,
    lastUpdated: '2023-07-15T14:30:00Z',
    tags: ['react', 'typescript', 'vite', 'tailwind'],
    official: true,
  },
  { 
    id: 'nextjs-starter', 
    name: 'Next.js Starter', 
    description: 'Production-ready Next.js project with TypeScript and Tailwind CSS',
    category: 'nextjs',
    stars: 2890,
    downloads: 12456,
    lastUpdated: '2023-08-01T09:15:00Z',
    tags: ['nextjs', 'typescript', 'tailwind', 'ssr'],
    official: true,
  },
  { 
    id: 'vue3-ts', 
    name: 'Vue 3 + TypeScript', 
    description: 'Vue 3 Composition API with TypeScript and Vite',
    category: 'vue',
    stars: 876,
    downloads: 3210,
    lastUpdated: '2023-07-20T16:45:00Z',
    tags: ['vue', 'typescript', 'vite', 'composition-api'],
    official: true,
  },
  { 
    id: 'sveltekit', 
    name: 'SvelteKit', 
    description: 'SvelteKit with TypeScript and Tailwind CSS',
    category: 'svelte',
    stars: 1450,
    downloads: 5876,
    lastUpdated: '2023-07-25T11:20:00Z',
    tags: ['svelte', 'sveltekit', 'typescript', 'tailwind'],
    official: false,
  },
  { 
    id: 'express-api', 
    name: 'Express API', 
    description: 'RESTful API with Express.js and TypeScript',
    category: 'backend',
    stars: 654,
    downloads: 2890,
    lastUpdated: '2023-06-30T13:10:00Z',
    tags: ['nodejs', 'express', 'typescript', 'api'],
    official: true,
  },
];

const categories = [
  { id: 'all', name: 'All Templates' },
  { id: 'react', name: 'React' },
  { id: 'nextjs', name: 'Next.js' },
  { id: 'vue', name: 'Vue' },
  { id: 'svelte', name: 'Svelte' },
  { id: 'backend', name: 'Backend' },
  { id: 'official', name: 'Official' },
];

export default function TemplatesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('all');
  const navigate = useNavigate();

  // Simulate loading data
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 800);

    return () => clearTimeout(timer);
  }, []);

  const filteredTemplates = mockTemplates.filter(template => {
    const matchesSearch = 
      template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      template.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = 
      activeCategory === 'all' || 
      (activeCategory === 'official' ? template.official : template.category === activeCategory);
    
    return matchesSearch && matchesCategory;
  });

  const formatNumber = (num: number): string => {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-8rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between space-y-4 md:flex-row md:items-center md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Templates</h1>
          <p className="text-muted-foreground">
            Browse and manage project templates
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Template
        </Button>
      </div>

      <Card>
        <CardHeader className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
          <div className="relative w-full max-w-md">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search templates..."
              className="pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm">
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs 
            defaultValue="all" 
            className="w-full"
            onValueChange={(value) => setActiveCategory(value)}
          >
            <div className="overflow-x-auto pb-2">
              <TabsList className="w-full justify-start bg-transparent p-0">
                {categories.map((category) => (
                  <TabsTrigger 
                    key={category.id} 
                    value={category.id}
                    className="data-[state=active]:border-b-2 data-[state=active]:border-b-primary data-[state=active]:shadow-none rounded-none border-b-2 border-transparent px-4 py-2"
                  >
                    {category.name}
                  </TabsTrigger>
                ))}
              </TabsList>
            </div>
          </Tabs>

          {filteredTemplates.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <FileText className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">No templates found</h3>
              <p className="text-sm text-muted-foreground mt-1">
                {searchTerm ? 'Try adjusting your search or filter' : 'No templates available'}
              </p>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTemplates.map((template) => (
                <Card key={template.id} className="overflow-hidden hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{template.name}</CardTitle>
                      {template.official && (
                        <Badge variant="outline" className="border-primary/20 bg-primary/10 text-primary">
                          Official
                        </Badge>
                      )}
                    </div>
                    <CardDescription className="line-clamp-2 h-10">
                      {template.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pb-3">
                    <div className="flex flex-wrap gap-2 mb-4">
                      {template.tags.map((tag) => (
                        <Badge key={tag} variant="secondary" className="font-mono text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center">
                          <Star className="mr-1 h-3.5 w-3.5" />
                          <span>{formatNumber(template.stars)}</span>
                        </div>
                        <div className="flex items-center">
                          <Download className="mr-1 h-3.5 w-3.5" />
                          <span>{formatNumber(template.downloads)}</span>
                        </div>
                      </div>
                      <div className="text-xs">
                        Updated {formatDate(template.lastUpdated)}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="border-t px-6 py-3">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full"
                      onClick={() => navigate(`/templates/${template.id}`)}
                    >
                      <GitBranch className="mr-2 h-4 w-4" />
                      Use Template
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
