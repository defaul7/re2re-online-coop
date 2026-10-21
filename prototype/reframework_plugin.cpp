#include <reframework/API.h>

extern "C" __declspec(dllexport)
void reframework_plugin_required_version(REFrameworkPluginVersion* version) {
    if (version == nullptr) {
        return;
    }

    version->major = REFRAMEWORK_PLUGIN_VERSION_MAJOR;
    version->minor = REFRAMEWORK_PLUGIN_VERSION_MINOR;
    version->patch = REFRAMEWORK_PLUGIN_VERSION_PATCH;
}

static void on_lua_state_created(lua_State*) {
    // The callback runs when REFramework creates a Lua state.
    // Keep this callback diagnostic-only for the first prototype.
}

static void on_lua_state_destroyed(lua_State*) {
    // No Lua operations are performed during teardown.
}

extern "C" __declspec(dllexport)
bool reframework_plugin_initialize(
    const REFrameworkPluginInitializeParam* param
) {
    if (param == nullptr || param->functions == nullptr) {
        return false;
    }

    const auto* functions = param->functions;

    if (functions->log_info != nullptr) {
        functions->log_info(
            "[RE2 Online Coop] Diagnostic plugin initialization started"
        );
    }

    if (functions->on_lua_state_created == nullptr ||
        functions->on_lua_state_destroyed == nullptr) {
        if (functions->log_error != nullptr) {
            functions->log_error(
                "[RE2 Online Coop] Required Lua callbacks are unavailable"
            );
        }
        return false;
    }

    const bool created_registered =
        functions->on_lua_state_created(on_lua_state_created);

    const bool destroyed_registered =
        functions->on_lua_state_destroyed(on_lua_state_destroyed);

    if (!created_registered || !destroyed_registered) {
        if (functions->log_error != nullptr) {
            functions->log_error(
                "[RE2 Online Coop] Failed to register Lua callbacks"
            );
        }
        return false;
    }

    if (functions->log_info != nullptr) {
        functions->log_info(
            "[RE2 Online Coop] Diagnostic plugin initialized successfully"
        );
    }

    return true;
}
