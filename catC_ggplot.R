# Install patchwork if not already installed
if (!requireNamespace("patchwork", quietly = TRUE)) {
  install.packages("patchwork")
}

# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(viridis)
library(patchwork)

# Updated dataset
data <- data.frame(
  Organism = rep(c("Anthocerotibacter panamensis C109", "Myxosarcina sp.", "Scytonema tolypothrichoides VB-61278"), each = 4),
  AssemblyProcess = rep(paste("Assembly", 1:4), times = 3),
  CheckM_completeness = c(98.29, 98.29, 98.29, 98.29, 99.56, 99.34, 99.56, 99.56, 89.6, 88.88, 99.52, 99.76),
  Contamination = c(0.85, 0.85, 0.85, 0.85, 2.4, 2.84, 0.87, 0.87, 4.18, 2.49, 1.04, 1.04),
  Heterogeneity = c(0, 0, 0, 0, 58.33, 64.29, 0, 0, 76.92, 61.54, 0, 0),
  No_of_Contigs = c(1, 1, 2, 3, 35, 38, 75, 26, 467, 455, 148, 41),
  Genome_size = c(4, 4, 4.1, 4.1, 6.3, 6.3, 6.1, 6.3, 8.7, 8.6, 9.8, 9.9),
  Busco_completeness = c(88.7, 88.60, 88.7,88.7, 99.3, 98.7, 99.4, 99.4, 87.6, 86.6, 99.2, 99.5)
)
# Map AssemblyProcess to new labels
data$AssemblyProcess <- factor(data$AssemblyProcess,
                                levels = paste("Assembly", 1:4),
                                labels = c("Nocon assembly", "Lowcon assembly", "Highcon assembly", "HighconHetero assembly"))

# Set the levels for the Organism factor to maintain the original order
data$Organism <- factor(data$Organism, levels = unique(data$Organism))

# Function to create a plot for each organism
create_plot <- function(organism) {
  # Filter data for the current organism
  filtered_data <- data %>% filter(Organism == organism)

  # Reshape data for ggplot
  plot_data <- filtered_data %>%
    pivot_longer(cols = c(CheckM_completeness, Contamination, Heterogeneity, No_of_Contigs, Genome_size, Busco_completeness),
                 names_to = "Parameter", values_to = "Value")

  # Plot using ggplot
  p <- ggplot(plot_data, aes(x = Parameter, y = AssemblyProcess, color = Value, size = Value)) +
    geom_point() +
    scale_color_gradient(low = "blue", high = "red") +
    theme_minimal() +
    labs(title = paste(organism),
         x = NULL, # Remove x-axis label
         y = NULL, # Remove y-axis label
         color = "Value",
         size = "Value") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          plot.title = element_text(size = 10),  # Adjust the title font size here
         legend.position = "none")  # Remove the legend
  return(p)
}

# List of organisms
organisms <- unique(data$Organism)

# Create a list of plots
plots <- lapply(organisms, create_plot)
# Combine plots using patchwork in a grid layout
combined_plot <- wrap_plots(plots) +
  plot_layout(ncol = 4, byrow = TRUE)  # Arrange in 1 row

# Save the combined plot as a single PDF
ggsave(filename = "C.pdf", plot = combined_plot, width = 15, height = 4)

