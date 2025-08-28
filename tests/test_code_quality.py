#!/usr/bin/env python3
"""
@author: Aleph Aseffa
Code Quality Tests for Monopoly UI

Tests that can run without tkinter to verify code structure and quality.
"""

import unittest
import os
import sys
import ast
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCodeStructure(unittest.TestCase):
    """Test code structure and quality without GUI dependencies"""
    
    def test_all_files_exist(self):
        """Test that all required files exist"""
        required_files = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py",
            "polished_launcher.py",
            "tests/test_monopoly_ui.py"
        ]
        
        for file_path in required_files:
            self.assertTrue(
                os.path.exists(file_path),
                f"Required file {file_path} does not exist"
            )
    
    def test_colors_module_structure(self):
        """Test colors.py module structure"""
        with open("gui/colors.py", "r") as f:
            tree = ast.parse(f.read())
        
        # Check for required dictionaries
        required_dicts = ["PROPERTY_COLORS", "BOARD_COLORS", "UI_COLORS", 
                         "SIZES", "FONTS", "ANIMATION"]
        
        module_vars = [node.targets[0].id for node in ast.walk(tree) 
                      if isinstance(node, ast.Assign) and 
                      isinstance(node.targets[0], ast.Name)]
        
        for var_name in required_dicts:
            self.assertIn(var_name, module_vars, 
                         f"Required dictionary {var_name} not found in colors.py")
        
        # Check for required functions
        required_functions = ["get_property_color", "get_player_color", 
                            "darken_color", "lighten_color"]
        
        function_names = [node.name for node in ast.walk(tree) 
                         if isinstance(node, ast.FunctionDef)]
        
        for func_name in required_functions:
            self.assertIn(func_name, function_names,
                         f"Required function {func_name} not found in colors.py")
    
    def test_authentic_board_class_structure(self):
        """Test authentic_board.py class structure"""
        with open("gui/authentic_board.py", "r") as f:
            tree = ast.parse(f.read())
        
        # Find AuthenticMonopolyBoard class
        classes = [node for node in ast.walk(tree) 
                  if isinstance(node, ast.ClassDef)]
        
        self.assertTrue(len(classes) > 0, "No classes found in authentic_board.py")
        
        board_class = None
        for cls in classes:
            if cls.name == "AuthenticMonopolyBoard":
                board_class = cls
                break
        
        self.assertIsNotNone(board_class, 
                           "AuthenticMonopolyBoard class not found")
        
        # Check for essential methods
        required_methods = [
            "__init__", "_render_board", "_draw_space", 
            "add_player_token", "move_player_token"
        ]
        
        method_names = [node.name for node in board_class.body 
                       if isinstance(node, ast.FunctionDef)]
        
        for method in required_methods:
            self.assertIn(method, method_names,
                         f"Required method {method} not found in AuthenticMonopolyBoard")
    
    def test_panel_classes_exist(self):
        """Test that all panel classes exist in polished_panels.py"""
        with open("gui/polished_panels.py", "r") as f:
            tree = ast.parse(f.read())
        
        required_classes = [
            "MonopolyPlayerPanel",
            "MonopolyControlPanel",
            "MonopolyPropertyCard",
            "MonopolyGameLog"
        ]
        
        class_names = [node.name for node in ast.walk(tree) 
                      if isinstance(node, ast.ClassDef)]
        
        for cls_name in required_classes:
            self.assertIn(cls_name, class_names,
                         f"Required class {cls_name} not found in polished_panels.py")
    
    def test_main_gui_class_structure(self):
        """Test polished_monopoly_gui.py structure"""
        with open("gui/polished_monopoly_gui.py", "r") as f:
            tree = ast.parse(f.read())
        
        # Check for PolishedMonopolyGUI class
        classes = [node.name for node in ast.walk(tree) 
                  if isinstance(node, ast.ClassDef)]
        
        self.assertIn("PolishedMonopolyGUI", classes,
                     "PolishedMonopolyGUI class not found")
        
        # Find the class
        gui_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "PolishedMonopolyGUI":
                gui_class = node
                break
        
        # Check for essential methods
        required_methods = [
            "__init__", "_create_main_layout", "_start_new_game",
            "run", "_on_roll_dice", "_on_property_click"
        ]
        
        method_names = [n.name for n in gui_class.body 
                       if isinstance(n, ast.FunctionDef)]
        
        for method in required_methods:
            self.assertIn(method, method_names,
                         f"Required method {method} not found in PolishedMonopolyGUI")
    
    def test_no_syntax_errors(self):
        """Test that all Python files have valid syntax"""
        python_files = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py",
            "polished_launcher.py"
        ]
        
        for file_path in python_files:
            with open(file_path, "r") as f:
                try:
                    compile(f.read(), file_path, 'exec')
                except SyntaxError as e:
                    self.fail(f"Syntax error in {file_path}: {e}")
    
    def test_docstrings_present(self):
        """Test that modules and classes have docstrings"""
        python_files = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py"
        ]
        
        for file_path in python_files:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())
            
            # Check module docstring
            self.assertIsInstance(tree.body[0], ast.Expr,
                                f"No module docstring in {file_path}")
            self.assertIsInstance(tree.body[0].value, ast.Constant,
                                f"No module docstring in {file_path}")
            
            # Check class docstrings
            classes = [node for node in ast.walk(tree) 
                      if isinstance(node, ast.ClassDef)]
            
            for cls in classes:
                if cls.body and isinstance(cls.body[0], ast.Expr) and \
                   isinstance(cls.body[0].value, ast.Constant):
                    continue  # Has docstring
                else:
                    self.fail(f"Class {cls.name} in {file_path} lacks docstring")
    
    def test_color_values_valid(self):
        """Test that color values are valid hex codes"""
        import re
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        
        with open("gui/colors.py", "r") as f:
            content = f.read()
        
        # Extract color values using regex
        color_pattern = re.compile(r'"(#[0-9A-Fa-f]{6})"')
        colors = color_pattern.findall(content)
        
        self.assertGreater(len(colors), 0, "No color values found")
        
        for color in colors:
            self.assertTrue(hex_pattern.match(color),
                          f"Invalid hex color: {color}")
    
    def test_proper_imports(self):
        """Test that imports are properly structured"""
        files_to_check = [
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py"
        ]
        
        for file_path in files_to_check:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())
            
            # Check for colors import
            imports = [node for node in ast.walk(tree)
                      if isinstance(node, ast.ImportFrom)]
            
            has_colors_import = any(
                imp.module and "colors" in imp.module 
                for imp in imports
            )
            
            self.assertTrue(has_colors_import,
                          f"{file_path} doesn't import from colors module")


class TestCodeQuality(unittest.TestCase):
    """Test code quality metrics"""
    
    def test_line_length(self):
        """Test that lines don't exceed reasonable length"""
        MAX_LINE_LENGTH = 120  # PEP 8 recommends 79, but 120 is reasonable
        
        files_to_check = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py"
        ]
        
        for file_path in files_to_check:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                # Skip comment lines and docstrings
                if line.strip().startswith('#') or line.strip().startswith('"""'):
                    continue
                    
                if len(line.rstrip()) > MAX_LINE_LENGTH:
                    # Allow some longer lines but warn
                    if len(line.rstrip()) > 150:
                        self.fail(f"Line {i} in {file_path} exceeds max length: {len(line.rstrip())} chars")
    
    def test_no_debug_code(self):
        """Test that no debug print statements are left in code"""
        files_to_check = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py"
        ]
        
        debug_patterns = ["print(", "console.log", "debugger", "pdb.set_trace"]
        
        for file_path in files_to_check:
            with open(file_path, "r") as f:
                content = f.read()
            
            for pattern in debug_patterns:
                # Allow print in docstrings and comments
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if pattern in line and not line.strip().startswith('#'):
                        # Check if it's in a docstring
                        if '"""' not in line and "'''" not in line:
                            # Allow some specific prints (like in main)
                            if file_path == "polished_launcher.py" and pattern == "print(":
                                continue
                            self.fail(f"Debug code '{pattern}' found in {file_path} line {i}")
    
    def test_consistent_naming(self):
        """Test that naming conventions are followed"""
        with open("gui/authentic_board.py", "r") as f:
            tree = ast.parse(f.read())
        
        # Check class names (PascalCase)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.assertTrue(node.name[0].isupper(),
                              f"Class {node.name} should start with uppercase")
        
        # Check function names (snake_case)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private methods
                    # Allow setUp, tearDown for tests
                    if node.name not in ['setUp', 'tearDown']:
                        self.assertTrue('_' in node.name or node.name.islower(),
                                      f"Function {node.name} should use snake_case")


class TestDocumentation(unittest.TestCase):
    """Test documentation quality"""
    
    def test_author_attribution(self):
        """Test that all files have author attribution"""
        files_to_check = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py",
            "polished_launcher.py"
        ]
        
        for file_path in files_to_check:
            with open(file_path, "r") as f:
                content = f.read()
            
            self.assertIn("@author: Aleph Aseffa", content,
                         f"Author attribution missing in {file_path}")
    
    def test_file_headers(self):
        """Test that files have proper header documentation"""
        files_to_check = [
            "gui/colors.py",
            "gui/authentic_board.py",
            "gui/polished_panels.py",
            "gui/polished_monopoly_gui.py"
        ]
        
        for file_path in files_to_check:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            # Check that file starts with docstring
            has_docstring = False
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                if '"""' in line:
                    has_docstring = True
                    break
            
            self.assertTrue(has_docstring,
                          f"No file header docstring in {file_path}")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)