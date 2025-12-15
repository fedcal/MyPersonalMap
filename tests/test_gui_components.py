"""
Test GUI Components

Verifica che tutti i componenti GUI possano essere instanziati correttamente.
Questi test NON richiedono un display server.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_theme_loading():
    """Test che il tema possa essere caricato correttamente."""
    try:
        from pymypersonalmap.gui.theme import COLORS, SPACING, FONTS, get_font

        # Verifica colori
        assert COLORS is not None
        assert 'primary' in COLORS
        assert COLORS['primary'] == '#4F46E5'

        # Verifica spacing
        assert SPACING is not None
        assert 'xs' in SPACING

        # Verifica fonts
        assert FONTS is not None
        assert 'sans' in FONTS
        assert 'mono' in FONTS

        # Verifica get_font
        font = get_font(size=14)
        assert font is not None

        print("✓ Theme loading test passed")
    except Exception as e:
        print(f"Theme loading error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def test_config_manager():
    """Test ConfigManager per gestione configurazioni."""
    from pymypersonalmap.gui.config_manager import ConfigManager

    config_mgr = ConfigManager()

    # Verifica user data directory
    user_dir = config_mgr.get_user_data_dir()
    assert user_dir is not None
    assert isinstance(user_dir, Path)

    # Verifica env path
    env_path = config_mgr.get_env_path()
    assert env_path is not None
    assert isinstance(env_path, Path)

    print("✓ ConfigManager test passed")


def test_backend_manager_init():
    """Test inizializzazione BackendManager (senza avviare server)."""
    from pymypersonalmap.gui.backend_manager import BackendManager

    backend = BackendManager(host="127.0.0.1", port=8000)

    # Verifica attributi
    assert backend.host == "127.0.0.1"
    assert backend.port == 8000
    assert backend.is_running is False
    assert backend.server_thread is None

    print("✓ BackendManager initialization test passed")


def test_component_classes_importable():
    """Test che tutte le classi componenti siano importabili."""
    components_to_test = [
        ('pymypersonalmap.gui.components.custom_button', 'CustomButton'),
        ('pymypersonalmap.gui.components.custom_sidebar', 'Sidebar'),  # Fixed: class is named Sidebar
        ('pymypersonalmap.gui.components.map_viewer', 'MapViewer'),
        ('pymypersonalmap.gui.layouts.main_layout', 'MainLayout'),
        ('pymypersonalmap.gui.setup_wizard', 'DatabaseSetupWizard'),  # Fixed: class is named DatabaseSetupWizard
        ('pymypersonalmap.gui.splash', 'SplashScreen'),
        ('pymypersonalmap.gui.splash', 'SplashScreenDark'),
    ]

    for module_path, class_name in components_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            assert component_class is not None
            print(f"✓ {class_name} importable")
        except Exception as e:
            print(f"✗ {class_name} import failed: {e}")
            raise


def test_settings_config():
    """Test che settings.py carichi correttamente le configurazioni."""
    from pymypersonalmap.config import settings

    # Verifica variabili critiche
    assert hasattr(settings, 'DATABASE_USER')
    assert hasattr(settings, 'DATABASE_PASSWORD')
    assert hasattr(settings, 'DATABASE_URL')
    assert hasattr(settings, 'DATABASE_NAME')
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'SERVER_HOST')
    assert hasattr(settings, 'SERVER_PORT')

    # Verifica computed database_url
    assert hasattr(settings, 'database_url')
    assert 'mysql+pymysql' in settings.database_url

    print("✓ Settings configuration test passed")


def test_models_importable():
    """Test che i modelli database siano importabili."""
    from pymypersonalmap.models import Marker, Label, MarkerLabel

    assert Marker is not None
    assert Label is not None
    assert MarkerLabel is not None

    print("✓ Models import test passed")


def run_all_tests():
    """Esegue tutti i test."""
    print("=" * 60)
    print("Testing GUI Components")
    print("=" * 60)

    tests = [
        ("Theme Loading", test_theme_loading),
        ("Config Manager", test_config_manager),
        ("Backend Manager Init", test_backend_manager_init),
        ("Component Classes", test_component_classes_importable),
        ("Settings Config", test_settings_config),
        ("Models Import", test_models_importable),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\n[TEST] {test_name}...")
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
