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
  Organism = rep(c("Nostoc edaphicum CCNP1411", "Candidatus Paraprochloron terpiosi LD05", "Tolypothrix bouteillei vb52130", "simulated category B"), each = 4),
  AssemblyProcess = rep(paste("Assembly", 1:4), times = 4),
  CheckM_completeness = c(99.7, 99.7, 99.7, 99.7, 96.89, 96.89, 96.22, 96.67, 99.66, 99.66, 99.76, 99.52, 99.97, 99.97, 99.97, 99.97),
  Contamination = c(1.33, 1.33, 1.33, 1.78, 0.52, 0.52, 0.52, 1.19, 1.04, 1.29, 1.29, 1.67, 0.45, 0.09, 0.04, 0.09),
  Heterogeneity = c(0, 0, 0, 23.08, 0, 0, 0, 50, 0, 0, 0, 36.36, 40, 0, 0, 0),
  No_of_Contigs = c(14, 20, 35, 22, 1, 1, 96, 102, 21, 20, 66, 40, 6, 3, 18, 47),
  Genome_size = c(9.5, 9.8, 8.5, 8.3, 3.7, 3.7, 3.5, 3.6, 11, 11, 11, 12, 5.6, 5.6, 5.3, 5.5),
  Busco_completeness = c(99.7, 99.7, 99.9, 99.9, 92.3, 92.4, 91.6, 92.3, 99.1, 99.2, 99.6, 99.3, 100, 100, 100, 100))
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
ggsave(filename = "B.pdf", plot = combined_plot, width = 15, height = 4)

