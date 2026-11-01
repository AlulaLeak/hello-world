#!/usr/bin/env python3
from pathlib import Path
import sys, re

root = Path(sys.argv[1]).resolve()

def read(rel):
    return (root / rel).read_text()

def write(rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

# --- Identity / update compatibility -----------------------------------------------------------
gradle = read("app/build.gradle.kts")
gradle = gradle.replace('applicationId = "com.andrerinas.headunitrevived"', 'applicationId = "app.earpiece.headunit"')
gradle = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 5', gradle, count=1)
gradle = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.1.0-premium1"', gradle, count=1)
gradle = gradle.replace('isMinifyEnabled = true', 'isMinifyEnabled = false')
gradle = gradle.replace('isShrinkResources = true', 'isShrinkResources = false')
write("app/build.gradle.kts", gradle)

manifest = read("app/src/main/AndroidManifest.xml")
manifest = manifest.replace(
    'android:name="com.andrerinas.openheadunit.permission.NAVIGATION_UPDATE"',
    'android:name="app.earpiece.headunit.permission.NAVIGATION_UPDATE"'
)
write("app/src/main/AndroidManifest.xml", manifest)

strings = read("app/src/main/res/values/strings.xml")
strings = re.sub(r'<string name="title">.*?</string>', '<string name="title">Earpiece Auto</string>', strings, count=1)
strings = re.sub(r'<string name="home_action_back_to_android_auto">.*?</string>',
                 '<string name="home_action_back_to_android_auto">Resume Android Auto</string>', strings, count=1)
# Make the active hero read like the approved concept.
strings = re.sub(r'<string name="home_kicker_active">.*?</string>',
                 '<string name="home_kicker_active">CONNECTED</string>', strings, count=1)
strings = re.sub(r'<string name="home_title_active">.*?</string>',
                 '<string name="home_title_active">Phone connected</string>', strings, count=1)
write("app/src/main/res/values/strings.xml", strings)

# --- Premium palette --------------------------------------------------------------------------
colors = read("app/src/main/res/values/colors.xml")
replacements = {
    'home_panel': '#C8121A34',
    'home_panel_stroke': '#664A7DFF',
    'home_tile': '#C8172442',
    'home_tile_pressed': '#E02A3B68',
    'home_tile_stroke': '#334A7DFF',
    'home_slot_stroke': '#556B7FFF',
    'home_text': '#FFF8FBFF',
    'home_text_muted': '#FFB9C6E8',
    'home_apps_tile': '#D8125FD7',
    'home_apps_tile_pressed': '#F01B70F0',
    'home_apps_icon': '#FFFFFFFF',
    'home_usb': '#FF5AA8FF',
    'home_wifi': '#FF5B7CFF',
    'home_self': '#FF8A5CFF',
    'home_monochrome': '#FF9DB0D6',
}
for name, value in replacements.items():
    colors = re.sub(fr'<color name="{name}">.*?</color>', f'<color name="{name}">{value}</color>', colors)
write("app/src/main/res/values/colors.xml", colors)

# Night resources override the same roles on dark screens. Make them match the premium theme.
night = root / "app/src/main/res/values-night/colors.xml"
if night.exists():
    n = night.read_text()
    for name, value in replacements.items():
        n = re.sub(fr'<color name="{name}">.*?</color>', f'<color name="{name}">{value}</color>', n)
    night.write_text(n)

# --- Premium geometry for a 1024x600 class screen ---------------------------------------------
# Existing qualified dimen resources still govern tiny/portrait displays. Add an exact-ish
# landscape qualifier that wins on the user's head unit without disturbing other screens.
write("app/src/main/res/values-w900dp-h500dp/dimens.xml", """<resources>
    <dimen name="home_gap">12dp</dimen>
    <dimen name="home_panel_radius">24dp</dimen>
    <dimen name="home_tile_radius">18dp</dimen>
    <dimen name="home_tile_size">86dp</dimen>
    <dimen name="home_tile_icon">30dp</dimen>
    <dimen name="home_tile_label">12sp</dimen>
    <dimen name="home_card_padding_h">26dp</dimen>
    <dimen name="home_card_padding_v">20dp</dimen>
    <dimen name="home_card_icon_tile">58dp</dimen>
    <dimen name="home_card_icon">30dp</dimen>
    <dimen name="home_card_kicker">11sp</dimen>
    <dimen name="home_card_title">28sp</dimen>
    <dimen name="home_card_subtitle">15sp</dimen>
    <dimen name="home_cta_height">58dp</dimen>
    <dimen name="home_cta_min_width">260dp</dimen>
    <dimen name="home_progress_shine_width">44dp</dimen>
    <dimen name="home_cta_text">17sp</dimen>
    <dimen name="home_secondary_cta_height">42dp</dimen>
    <dimen name="home_secondary_cta_text">13sp</dimen>
    <dimen name="home_countdown_size">42dp</dimen>
    <dimen name="home_countdown_text">16sp</dimen>
    <dimen name="home_favorites_height">98dp</dimen>
    <dimen name="home_dots_height">18dp</dimen>
    <dimen name="home_dot_size">7dp</dimen>
    <dimen name="home_dot_active_width">20dp</dimen>
    <dimen name="home_dot_touch_width">38dp</dimen>
    <dimen name="home_favorite_icon">34dp</dimen>
    <dimen name="home_info_time">24sp</dimen>
    <dimen name="home_info_date">13sp</dimen>
    <dimen name="home_info_speed">20sp</dimen>
    <dimen name="home_info_gap_wide">10dp</dimen>
    <dimen name="home_info_min_text">120dp</dimen>
    <dimen name="home_widget_padding">6dp</dimen>
    <dimen name="home_widget_strip_min">120dp</dimen>
    <dimen name="home_widget_strip_max">160dp</dimen>
</resources>
""")

# --- Premium drawables ------------------------------------------------------------------------
write("app/src/main/res/drawable/premium_screen_bg.xml", """<?xml version="1.0" encoding="utf-8"?>
<gradient xmlns:android="http://schemas.android.com/apk/res/android"
    android:angle="315"
    android:startColor="#FF070C18"
    android:centerColor="#FF0B1831"
    android:endColor="#FF111B3D"
    android:type="linear" />
""")
write("app/src/main/res/drawable/premium_panel_bg.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="315" android:startColor="#D9182A55" android:endColor="#CC111A33" />
    <stroke android:width="1dp" android:color="#665D8EFF" />
    <corners android:radius="24dp" />
</shape>
""")
write("app/src/main/res/drawable/premium_rail_bg.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="270" android:startColor="#D90B1428" android:endColor="#C9152140" />
    <stroke android:width="1dp" android:color="#335A7FFF" />
    <corners android:radius="22dp" />
</shape>
""")
write("app/src/main/res/drawable/premium_hero_bg.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="0" android:startColor="#E4122B5C" android:centerColor="#E3193978" android:endColor="#D7271D68" />
    <stroke android:width="1dp" android:color="#885A8BFF" />
    <corners android:radius="26dp" />
</shape>
""")
write("app/src/main/res/drawable/premium_tile_bg.xml", """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <shape android:shape="rectangle">
            <gradient android:angle="315" android:startColor="#EF274778" android:endColor="#E5292C61" />
            <stroke android:width="1dp" android:color="#886A91FF" />
            <corners android:radius="18dp" />
        </shape>
    </item>
    <item>
        <shape android:shape="rectangle">
            <gradient android:angle="315" android:startColor="#D8192B50" android:endColor="#C916203D" />
            <stroke android:width="1dp" android:color="#445A7FFF" />
            <corners android:radius="18dp" />
        </shape>
    </item>
</selector>
""")

# --- Home XML: preserve every controller ID, modernize the structure ----------------------------
home = read("app/src/main/res/layout/fragment_home.xml")
home = home.replace('android:padding="@dimen/home_gap"', 'android:padding="14dp"', 1)
# Outer background gives the cockpit its new appearance.
home = home.replace('android:showDividers="middle">', 'android:showDividers="middle"\n    android:background="@drawable/premium_screen_bg">', 1)
# Driver rail gets premium glass panel.
home = home.replace('android:background="@drawable/home_panel_bg"', 'android:background="@drawable/premium_rail_bg"', 1)
# Hide the legacy Exit tile on the 1024x600 premium screen but keep the ID alive.
home = home.replace('android:id="@+id/exit_button"\n            style="@style/HomeTile">',
                    'android:id="@+id/exit_button"\n            style="@style/HomeTile"\n            android:visibility="gone">')
write("app/src/main/res/layout/fragment_home.xml", home)

# The controller repaints backgrounds dynamically; update its night card and tile factories so the
# premium look survives every state change rather than only the first frame.
helper_path = "app/src/main/java/com/andrerinas/openheadunit/utils/HomeUiHelper.kt"
helper = read(helper_path)
helper = helper.replace(
'''        card.background = shape(palette.panel, panelRadius, palette.panelStroke, strokePx)
        iconTile?.background = rounded(withAlpha(color, ACCENT_WASH_ALPHA), tileRadius)''',
'''        card.background = GradientDrawable(
            GradientDrawable.Orientation.LEFT_RIGHT,
            intArrayOf(0xE4122B5C.toInt(), 0xE3193978.toInt(), 0xD7271D68.toInt())
        ).apply {
            cornerRadius = panelRadius
            setStroke(strokePx, 0x885A8BFF.toInt())
        }
        iconTile?.background = rounded(withAlpha(color, 0x55), tileRadius)'''
)
helper = helper.replace(
'''    private fun tileBackground(context: Context, palette: Palette): Drawable {
        val radius = context.resources.getDimension(R.dimen.home_tile_radius)
        val strokePx = dp(context, 1)
        return pressable(
            palette.ripple,
            { shape(palette.tile, radius, palette.tileStroke, strokePx) },
            { shape(palette.tilePressed, radius, palette.tileStroke, strokePx) }
        )
    }''',
'''    private fun tileBackground(context: Context, palette: Palette): Drawable {
        val radius = context.resources.getDimension(R.dimen.home_tile_radius)
        val strokePx = dp(context, 1)
        return pressable(
            palette.ripple,
            {
                GradientDrawable(GradientDrawable.Orientation.TL_BR,
                    intArrayOf(0xD8192B50.toInt(), 0xC916203D.toInt())).apply {
                    cornerRadius = radius
                    setStroke(strokePx, 0x445A7FFF.toInt())
                }
            },
            {
                GradientDrawable(GradientDrawable.Orientation.TL_BR,
                    intArrayOf(0xEF274778.toInt(), 0xE5292C61.toInt())).apply {
                    cornerRadius = radius
                    setStroke(strokePx, 0x886A91FF.toInt())
                }
            }
        )
    }'''
)
write(helper_path, helper)

# --- Premium left rail behaviour ---------------------------------------------------------------
# For the user's WiFi-only configuration the connection itself lives in the hero card. Turn the
# self-mode slot into an Audio shortcut while preserving the underlying ID and controller wiring.
fragment_path = "app/src/main/java/com/andrerinas/openheadunit/main/HomeFragment.kt"
frag = read(fragment_path)
frag = frag.replace(
'''        selfModeTile.setOnClickListener { onSelfModeClicked() }''',
'''        selfModeTile.setOnClickListener { showPremiumAudioMenu() }'''
)
# Install premium labels/icons once the view exists. This is intentionally visual-only; the IDs
# remain the same so every other path remains compatible.
frag = frag.replace(
'''        setupListeners()
    }

    override fun onViewCreated''',
'''        setupPremiumRail()
        setupListeners()
    }

    private fun setupPremiumRail() {
        // The user's production setup is Native WiFi. Keep the connection in the hero card and use
        // the rail for the things a driver/passenger actually reaches repeatedly.
        usbTile.visibility = View.GONE
        wifiTile.visibility = View.GONE
        selfModeTile.visibility = View.VISIBLE
        selfModeTile.findViewById<ImageView>(R.id.home_tile_icon)?.setImageResource(R.drawable.ic_headphones)
        (selfModeTile as? ViewGroup)?.let { tile ->
            (0 until tile.childCount).map { tile.getChildAt(it) }.filterIsInstance<TextView>().firstOrNull()?.text = "Audio"
        }
    }

    private fun showPremiumAudioMenu() {
        val settings = App.provide(requireContext()).settings
        val current = if (settings.enableAudioSink) "Car speakers" else "Phone / earpiece"
        val items = arrayOf("Car speakers", "Phone / earpiece")
        MaterialAlertDialogBuilder(requireContext(), R.style.DarkAlertDialog)
            .setTitle("Audio output · $current")
            .setItems(items) { _, which ->
                val useCar = which == 0
                settings.enableAudioSink = useCar
                // Earpiece mic stays on the phone in both modes.
                settings.useHeadUnitMicrophone = false
                ToastUtils.showToast(
                    requireContext(),
                    if (useCar) "Audio → car speakers" else "Audio → phone / earpiece",
                    Toast.LENGTH_SHORT,
                    force = true
                )
                if (commManager.isConnected) {
                    ContextCompat.startForegroundService(
                        requireContext(),
                        Intent(requireContext(), AapService::class.java).apply {
                            action = AapService.ACTION_DISCONNECT
                        }
                    )
                    viewLifecycleOwner.lifecycleScope.launch {
                        delay(700)
                        if (isAdded) onWifiClicked()
                    }
                }
            }
            .show()
    }

    override fun onViewCreated'''
)
# home_tile_icon isn't present on original layout; avoid relying on a child ID by replacing that
# line with first ImageView discovery.
frag = frag.replace(
'selfModeTile.findViewById<ImageView>(R.id.home_tile_icon)?.setImageResource(R.drawable.ic_headphones)',
'(selfModeTile as? ViewGroup)?.let { tile -> (0 until tile.childCount).map { tile.getChildAt(it) }.filterIsInstance<ImageView>().firstOrNull()?.setImageResource(R.drawable.ic_headphones) }'
)
write(fragment_path, frag)

# Keep the premium app dock available even when Earpiece Auto is not the Android HOME launcher.
# This preserves the user's Netflix/DuckDuckGo passenger shortcuts while Android Auto stays active.
helper = read(helper_path)
old_favorites = '''    fun applyFavoritesVisibility(rootView: View, isLauncherActive: Boolean, showFavorites: Boolean) {
        // The whole area, not only its rows: an empty area that is still visible keeps the gap
        // above it, and outside launcher mode the main button then ended short of the driver bar.
        rootView.findViewById<View>(R.id.home_favorites_area)?.visibility =
            if (isLauncherActive) View.VISIBLE else View.GONE
        rootView.findViewById<View>(R.id.home_favorites)?.visibility = if (isLauncherActive) View.VISIBLE else View.GONE
        rootView.findViewById<View>(R.id.home_primary_icon_tile)?.visibility =
            if (isLauncherActive) View.GONE else View.VISIBLE
        favoriteSlotIds.forEach {
            rootView.findViewById<View>(it)?.visibility = if (showFavorites) View.VISIBLE else View.GONE
        }
    }'''
new_favorites = '''    fun applyFavoritesVisibility(rootView: View, isLauncherActive: Boolean, showFavorites: Boolean) {
        // Premium Earpiece Auto keeps the dock visible even when it is not the system HOME app.
        rootView.findViewById<View>(R.id.home_favorites_area)?.visibility = View.VISIBLE
        rootView.findViewById<View>(R.id.home_favorites)?.visibility = View.VISIBLE
        rootView.findViewById<View>(R.id.home_primary_icon_tile)?.visibility = View.GONE
        favoriteSlotIds.forEach {
            rootView.findViewById<View>(it)?.visibility = if (showFavorites) View.VISIBLE else View.GONE
        }
    }'''
if old_favorites in helper:
    helper = helper.replace(old_favorites, new_favorites)
else:
    raise SystemExit("Could not locate applyFavoritesVisibility for premium dock patch")
write(helper_path, helper)

# --- First-run defaults: earpiece microphone + WiFi-first --------------------------------------
# Set only when preferences are still absent; updates preserve user choices.
settings_path = "app/src/main/java/com/andrerinas/openheadunit/utils/Settings.kt"
st = read(settings_path)
st = st.replace(
'''    var useHeadUnitMicrophone: Boolean
        get() = prefs.getBoolean("use-head-unit-microphone", true)''',
'''    var useHeadUnitMicrophone: Boolean
        get() = prefs.getBoolean("use-head-unit-microphone", false)'''
)
write(settings_path, st)

print("Premium patch applied")
