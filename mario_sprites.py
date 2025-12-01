"""
Sprite loading and parsing utilities for Mario game
Handles extraction of sprites from sprite sheets
"""
import pygame
import os

class MarioSprites:
    """Manages all Mario game sprites"""
    
    def __init__(self):
        self.sprites = {}
        self.sprite_cache = {}
        self.tile_size = 16  # Default tile size in pixels
        self.scale_factor = 2  # Scale sprites for better visibility
        
    def load_all(self):
        """Load all sprite sheets and extract sprites"""
        try:
            self.load_tiles()
            self.load_characters()
            self.load_koopas()
            self.load_items()
            return True
        except Exception as e:
            print(f"Error loading sprites: {e}")
            return False
    
    def load_tiles(self):
        """Load and extract tiles from tiles.png"""
        try:
            tiles_path = "characters/img/tiles.png"
            if not os.path.exists(tiles_path):
                print(f"Warning: {tiles_path} not found")
                return
            
            tiles_sheet = pygame.image.load(tiles_path).convert_alpha()
            sheet_width = tiles_sheet.get_width()
            sheet_height = tiles_sheet.get_height()
            
            # Common tile sizes in Mario games: 16x16
            tile_size = 16
            
            # Extract common tiles
            # Ground tiles (usually at top of sheet)
            self.sprites['ground'] = self.extract_tile(tiles_sheet, 0, 0, tile_size)
            self.sprites['ground_left'] = self.extract_tile(tiles_sheet, 0, 0, tile_size)
            self.sprites['ground_middle'] = self.extract_tile(tiles_sheet, tile_size, 0, tile_size)
            self.sprites['ground_right'] = self.extract_tile(tiles_sheet, tile_size * 2, 0, tile_size)
            
            # Brick blocks
            self.sprites['brick'] = self.extract_tile(tiles_sheet, 0, tile_size, tile_size)
            self.sprites['question_block'] = self.extract_tile(tiles_sheet, tile_size, tile_size, tile_size)
            self.sprites['used_block'] = self.extract_tile(tiles_sheet, tile_size * 2, tile_size, tile_size)
            
            # Try to extract more tiles if available
            for y in range(0, min(sheet_height, tile_size * 10), tile_size):
                for x in range(0, min(sheet_width, tile_size * 20), tile_size):
                    tile_key = f'tile_{x//tile_size}_{y//tile_size}'
                    if tile_key not in self.sprites:
                        tile = self.extract_tile(tiles_sheet, x, y, tile_size)
                        if tile and self.is_not_empty(tile):
                            self.sprites[tile_key] = tile
                            
        except Exception as e:
            print(f"Error loading tiles: {e}")
    
    def load_characters(self):
        """Load and extract Mario character sprites from characters.gif"""
        try:
            chars_path = "characters/img/characters.gif"
            if not os.path.exists(chars_path):
                print(f"Warning: {chars_path} not found")
                return
            
            chars_sheet = pygame.image.load(chars_path).convert_alpha()
            sheet_width = chars_sheet.get_width()
            sheet_height = chars_sheet.get_height()
            
            # Mario sprites are typically 16x16 or 16x32
            sprite_width = 16
            sprite_height = 16
            
            # Extract Mario sprites (assuming standard layout)
            # Small Mario - facing right
            self.sprites['mario_idle_r'] = self.extract_tile(chars_sheet, 0, 0, sprite_width, sprite_height)
            self.sprites['mario_walk1_r'] = self.extract_tile(chars_sheet, sprite_width, 0, sprite_width, sprite_height)
            self.sprites['mario_walk2_r'] = self.extract_tile(chars_sheet, sprite_width * 2, 0, sprite_width, sprite_height)
            self.sprites['mario_walk3_r'] = self.extract_tile(chars_sheet, sprite_width * 3, 0, sprite_width, sprite_height)
            self.sprites['mario_jump_r'] = self.extract_tile(chars_sheet, sprite_width * 4, 0, sprite_width, sprite_height)
            
            # Small Mario - facing left (flip right-facing sprites)
            self.sprites['mario_idle_l'] = pygame.transform.flip(self.sprites.get('mario_idle_r'), True, False)
            self.sprites['mario_walk1_l'] = pygame.transform.flip(self.sprites.get('mario_walk1_r'), True, False)
            self.sprites['mario_walk2_l'] = pygame.transform.flip(self.sprites.get('mario_walk2_r'), True, False)
            self.sprites['mario_walk3_l'] = pygame.transform.flip(self.sprites.get('mario_walk3_r'), True, False)
            self.sprites['mario_jump_l'] = pygame.transform.flip(self.sprites.get('mario_jump_r'), True, False)
            
            # Try to find more sprites by scanning
            for y in range(0, min(sheet_height, sprite_height * 10), sprite_height):
                for x in range(0, min(sheet_width, sprite_width * 20), sprite_width):
                    sprite = self.extract_tile(chars_sheet, x, y, sprite_width, sprite_height)
                    if sprite and self.is_not_empty(sprite):
                        # Store as generic sprite
                        key = f'char_{x//sprite_width}_{y//sprite_height}'
                        if key not in self.sprites:
                            self.sprites[key] = sprite
                            
        except Exception as e:
            print(f"Error loading characters: {e}")
    
    def load_koopas(self):
        """Load and extract Koopa enemy sprites"""
        try:
            koopas_path = "characters/img/koopas.png"
            if not os.path.exists(koopas_path):
                print(f"Warning: {koopas_path} not found")
                return
            
            koopas_sheet = pygame.image.load(koopas_path).convert_alpha()
            sheet_width = koopas_sheet.get_width()
            sheet_height = koopas_sheet.get_height()
            
            sprite_size = 16
            
            # Extract Koopa sprites
            self.sprites['koopa_walk1_r'] = self.extract_tile(koopas_sheet, 0, 0, sprite_size)
            self.sprites['koopa_walk2_r'] = self.extract_tile(koopas_sheet, sprite_size, 0, sprite_size)
            self.sprites['koopa_shell'] = self.extract_tile(koopas_sheet, sprite_size * 2, 0, sprite_size)
            
            # Flip for left-facing
            self.sprites['koopa_walk1_l'] = pygame.transform.flip(self.sprites.get('koopa_walk1_r'), True, False)
            self.sprites['koopa_walk2_l'] = pygame.transform.flip(self.sprites.get('koopa_walk2_r'), True, False)
            
            # Scan for more sprites
            for y in range(0, min(sheet_height, sprite_size * 10), sprite_size):
                for x in range(0, min(sheet_width, sprite_size * 20), sprite_size):
                    sprite = self.extract_tile(koopas_sheet, x, y, sprite_size)
                    if sprite and self.is_not_empty(sprite):
                        key = f'koopa_{x//sprite_size}_{y//sprite_size}'
                        if key not in self.sprites:
                            self.sprites[key] = sprite
                            
        except Exception as e:
            print(f"Error loading koopas: {e}")
    
    def load_items(self):
        """Load and extract item sprites (coins, mushrooms, etc.)"""
        try:
            items_path = "characters/img/Items.png"
            if not os.path.exists(items_path):
                print(f"Warning: {items_path} not found")
                return
            
            items_sheet = pygame.image.load(items_path).convert_alpha()
            sheet_width = items_sheet.get_width()
            sheet_height = items_sheet.get_height()
            
            sprite_size = 16
            
            # Extract common items
            self.sprites['coin1'] = self.extract_tile(items_sheet, 0, 0, sprite_size)
            self.sprites['coin2'] = self.extract_tile(items_sheet, sprite_size, 0, sprite_size)
            self.sprites['coin3'] = self.extract_tile(items_sheet, sprite_size * 2, 0, sprite_size)
            self.sprites['mushroom'] = self.extract_tile(items_sheet, 0, sprite_size, sprite_size)
            self.sprites['flower'] = self.extract_tile(items_sheet, sprite_size, sprite_size, sprite_size)
            self.sprites['star'] = self.extract_tile(items_sheet, sprite_size * 2, sprite_size, sprite_size)
            
            # Scan for more items
            for y in range(0, min(sheet_height, sprite_size * 10), sprite_size):
                for x in range(0, min(sheet_width, sprite_size * 20), sprite_size):
                    sprite = self.extract_tile(items_sheet, x, y, sprite_size)
                    if sprite and self.is_not_empty(sprite):
                        key = f'item_{x//sprite_size}_{y//sprite_size}'
                        if key not in self.sprites:
                            self.sprites[key] = sprite
                            
        except Exception as e:
            print(f"Error loading items: {e}")
    
    def extract_tile(self, sheet, x, y, width, height=None):
        """Extract a single tile from a sprite sheet"""
        if height is None:
            height = width
        
        # Check bounds
        if x + width > sheet.get_width() or y + height > sheet.get_height():
            return None
        
        # Create surface for tile
        tile = pygame.Surface((width, height), pygame.SRCALPHA)
        tile.blit(sheet, (0, 0), (x, y, width, height))
        
        # Scale if needed
        if self.scale_factor != 1:
            tile = pygame.transform.scale(tile, (width * self.scale_factor, height * self.scale_factor))
        
        return tile
    
    def is_not_empty(self, surface):
        """Check if a surface has any non-transparent pixels"""
        # Check a few sample pixels
        width, height = surface.get_size()
        for x in range(0, width, max(1, width // 4)):
            for y in range(0, height, max(1, height // 4)):
                if surface.get_at((x, y))[3] > 0:  # Check alpha channel
                    return True
        return False
    
    def get_sprite(self, name, default=None):
        """Get a sprite by name, with optional default fallback"""
        sprite = self.sprites.get(name)
        if sprite is None and default:
            return self.sprites.get(default)
        return sprite
    
    def get_scaled_sprite(self, name, scale):
        """Get a sprite scaled to a specific size"""
        sprite = self.get_sprite(name)
        if sprite is None:
            return None
        
        # Cache scaled versions
        cache_key = f"{name}_{scale}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
        
        original_size = sprite.get_size()
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        scaled = pygame.transform.scale(sprite, new_size)
        self.sprite_cache[cache_key] = scaled
        return scaled

