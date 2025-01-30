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
  Organism = rep(c("Gloeobacter morelensis MG652769", "Tolypothrix sp.PCC 7712", "Phormidium yuhuli AB48", "E.coli"), each = 4),
  AssemblyProcess = rep(paste("Assembly", 1:4), times = 4),
  CheckM_completeness = c(99.15, 99.15, 99.15, 99.15, 99.11, 99.11, 99.11, 98, 100, 100, 100, 74, 99.97, 99.97, 99.97, 99.97),
  Contamination = c(0.85, 0.85, 0.85, 0.85, 0, 0, 0, 0, 0.54, 0.54, 0.54, 0, 0.09, 0.09, 0.04, 0.09),
  Heterogeneity = c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
  No_of_Contigs = c(5, 1, 9, 28, 17, 20, 15, 219, 1, 1, 4, 200, 7, 3, 18, 47),
  Genome_size = c(5, 4.7, 4.8, 4.8, 9.8, 9.8, 9.9, 9.8, 4.6, 4.6, 4.7, 2.6, 6, 5.6, 5.3, 5.5),
  Busco_completeness = c(92, 92, 92.3, 92.1, 99.9, 99.9, 99.7, 99.8, 99.4, 99.3, 99.4, 42, 100, 100, 100, 100)
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
ggsave(filename = "A.pdf", plot = combined_plot, width = 15, height = 4)

