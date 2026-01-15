use zed_extension_api as zed;

struct WebDevelopmentToolsExtension;

impl zed::Extension for WebDevelopmentToolsExtension {
    fn context_server_command(
        &mut self,
        id: &zed::ContextServerId,
        _project: &zed::Project,
    ) -> zed::Result<zed::Command> {
        match id.0.as_str() {
            "web-development-mcp" => Ok(zed::Command {
                command: "uv".to_string(),
                args: vec!["run".to_string(), "web_development_mcp.__main__:main".to_string()],
                env: Default::default(),
            }),
            _ => Err(format!("Unknown server: {}", id.0)),
        }
    }
}

zed::register_extension!(WebDevelopmentToolsExtension);
