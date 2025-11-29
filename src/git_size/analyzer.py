"""Core Git repository analysis logic."""
import os
from pathlib import Path
from collections import defaultdict
from git import Repo
from git.exc import InvalidGitRepositoryError

class GitAnalyzer:
    def __init__(self, repo_path='.'):
        try:
            self.repo = Repo(repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            raise ValueError(f"Not a git repository: {repo_path}")
        
        self.repo_path = Path(self.repo.working_dir)
    
    def get_largest_files(self, limit=20, min_size=0, extensions=None):
        """Get largest files across all history."""
        file_sizes = {}
        
        for commit in self.repo.iter_commits('--all'):
            for item in commit.tree.traverse():
                if item.type == 'blob':
                    if extensions and not any(item.path.endswith(ext) for ext in extensions):
                        continue
                    
                    size = item.size
                    if size < min_size:
                        continue
                    
                    if item.path not in file_sizes or size > file_sizes[item.path]['size']:
                        file_sizes[item.path] = {
                            'path': item.path,
                            'size': size,
                            'sha': item.hexsha[:8],
                            'commit': commit.hexsha[:8]
                        }
        
        sorted_files = sorted(file_sizes.values(), key=lambda x: x['size'], reverse=True)
        return sorted_files[:limit]
    
    def get_largest_directories(self, limit=15):
        """Calculate size by directory."""
        dir_sizes = defaultdict(int)
        
        for commit in self.repo.iter_commits('--all'):
            for item in commit.tree.traverse():
                if item.type == 'blob':
                    dir_path = str(Path(item.path).parent)
                    if dir_path == '.':
                        dir_path = '(root)'
                    dir_sizes[dir_path] += item.size
        
        sorted_dirs = [{'path': path, 'size': size} for path, size in dir_sizes.items()]
        sorted_dirs.sort(key=lambda x: x['size'], reverse=True)
        return sorted_dirs[:limit]
    
    def get_deleted_files(self, limit=20):
        """Find deleted files still in history."""
        all_files = set()
        current_files = set()
        
        for commit in self.repo.iter_commits('--all'):
            for item in commit.tree.traverse():
                if item.type == 'blob':
                    all_files.add((item.path, item.size))
        
        try:
            for item in self.repo.head.commit.tree.traverse():
                if item.type == 'blob':
                    current_files.add(item.path)
        except ValueError:
            pass
        
        deleted = [{'path': path, 'size': size} for path, size in all_files if path not in current_files]
        deleted.sort(key=lambda x: x['size'], reverse=True)
        return deleted[:limit]
    
    def get_lfs_candidates(self, threshold):
        """Suggest files for Git LFS based on size."""
        candidates = []
        
        for commit in self.repo.iter_commits('--all'):
            for item in commit.tree.traverse():
                if item.type == 'blob' and item.size >= threshold:
                    candidates.append({
                        'path': item.path,
                        'size': item.size,
                        'sha': item.hexsha[:8]
                    })
        
        unique_candidates = {c['path']: c for c in candidates}
        sorted_candidates = sorted(unique_candidates.values(), key=lambda x: x['size'], reverse=True)
        return sorted_candidates
    
    def get_repo_stats(self):
        """Get overall repository statistics."""
        git_dir = self.repo_path / '.git'
        pack_size = 0
        object_count = 0
        
        pack_dir = git_dir / 'objects' / 'pack'
        if pack_dir.exists():
            for pack_file in pack_dir.glob('*.pack'):
                pack_size += pack_file.stat().st_size
                object_count += 1
        
        working_size = sum(f.stat().st_size for f in self.repo_path.rglob('*') if f.is_file() and '.git' not in str(f))
        
        commit_count = sum(1 for _ in self.repo.iter_commits('--all'))
        branch_count = len(list(self.repo.branches))
        
        return {
            'pack_size': pack_size,
            'object_count': object_count,
            'working_size': working_size,
            'commit_count': commit_count,
            'branch_count': branch_count
        }