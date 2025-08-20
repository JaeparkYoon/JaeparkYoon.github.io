package jpyoon.mediumsample

import android.content.Context
import android.content.res.Configuration
import android.os.Build
import android.os.Bundle
import android.util.DisplayMetrics
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import jpyoon.mediumsample.ui.theme.MediumSampleTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MediumSampleTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }

    override fun attachBaseContext(newBase: Context?) {
        val configuration = Configuration(newBase?.resources?.configuration)
        val currentDensityDpi = configuration.densityDpi
        configuration.densityDpi = if (currentDensityDpi >= DisplayMetrics.DENSITY_560 &&
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q
        ) {
            DisplayMetrics.DENSITY_560
        } else {
            DisplayMetrics.DENSITY_DEVICE_STABLE
        }
        val context = newBase?.createConfigurationContext(configuration)
        super.attachBaseContext(context)
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MediumSampleTheme {
        Greeting("Android")
    }
}